# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer


# =todo 63 (module-ui, ux) +0: basic layer control, on-off

from .AppWindow import *


class Ui():
	styleSelect = {
		'display':'',
		'opacity':'1',
		'fill':'#f80'
	}
	styleHover = {
		'display':'',
		'opacity':'1',
		'fill':'#f00'
	}


	args = None

	appWindow = None

	data = None
	qApp = None

	layerHover = None
	layersSelection = []



	def dispatchGetList(self):
		return self.dispatch.getDevices()



# -todo 88 (fix, gcode) +0: use dispatch both for file save
	def dispatchSend(self, _name):
		return self.dispatch.runDevice(_name, self.appWindow.dispatchLog)



	def storeWindow(self, _size, _maximized):
		self.args.set('wMaxi', _maximized)
		if not _maximized:
			self.args.set('wSize', (_size.width(),_size.height()) )



	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch

		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))
#  todo 50 (module-ui) +0: add style
#		with open('Ui/style.qss') as fQss:
#			self.qApp.setStyleSheet(fQss.read())


		uiFile = ('./Ui/AppWindow.ui')
		self.appWindow = AppWindow(uiFile)

		self.appWindow.sigResize.connect(self.storeWindow)
		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.sigAddFile.connect(self.addFile)
		self.appWindow.sigStoreG.connect(self.storeG)
		self.appWindow.setCBLayerSet(self.layerSet)

		self.appWindow.setCBConnList(self.dispatchGetList)
		self.appWindow.sigDispatch.connect(self.dispatchSend)



	def exec(self):
		self.appWindow.show()


		self.qApp.exec_()




	def addFile(self):
		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		self.layerHover = None
		self.layersSelection = []

		cData = self.data.loadXML(fileName)
		if cData:
			self.appWindow.reactAddFile(cData)
		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeG(self):
		if not self.data.info():
			print("No scene data")
			return


		cRecentA = self.args.get("recentSaved", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(None, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		h = self.appWindow.lViewport.canvas.docHeight
		with open(fileName, 'w') as f:
			f.write(self.data.getG(0, h))


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentSaved", cRecentA+[fileName])




	def layerSet(self, hover=False, selection=False):
		if not self.data:
			print ('No data')
			return


		if (hover != False):
			self.data.override(self.layerHover)

			self.layerHover = hover


		if selection != False:
			for l in self.layersSelection:
				self.data.override(l)

			self.layersSelection = selection


		for a in self.layersSelection:
			self.data.override(a, self.styleSelect)

# -todo 77 (fix, module-ui, viewport) +0: duplicate hover element topmost
		self.data.override(self.layerHover, self.styleHover)


		return self.data.getXML()
