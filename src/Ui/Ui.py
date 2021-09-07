# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer


from .AppWindow import *


class Ui():
	defUi = './Ui/AppWindow.ui'
	defStyle = './Ui/schemes/default dark.qss'


# =todo 101 (module-ui) +0: styles for selected-hovered-visible matrix


	args = None

	appWindow = None

	data = None
	qApp = None

# =todo 103 (module-ui, module-data, filter, API) +0: move geo decorators to data (filter)


	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch

		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))


		self.appWindow = AppWindow(self.defUi, self.defStyle)

		self.appWindow.sigResize.connect(self.storeWindow)
		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.sigAddFile.connect(self.addFile)
		self.appWindow.sigStoreG.connect(self.storeG)
		self.appWindow.sigLayerSelect.connect(self.layerSetSelect)
		self.appWindow.sigLayerHover.connect(self.layerSetHover)
		self.appWindow.sigCtrlLayersSet.connect(self.ctrlLayersSet)

		self.appWindow.connList(self.dispatch.getDevices())
		self.appWindow.sigDispatch.connect(self.dispatchSend)


		self.decorDefault = self.data.decorNew({
			'vector-effect': 'non-scaling-stroke',
			'stroke-width':'2px',
			'stroke':'#bbb',
			'fill':'#888',
			'opacity': 1
		}, -1)
		self.decorSelect = self.data.decorNew({
			'fill':'#bbb',
		})
		self.decorHover = self.data.decorNew({
			'stroke':'#fe9',
		}, 1)
		self.decorOff = self.data.decorNew({
			'opacity': .2
		}, 1)



	def exec(self):
		self.appWindow.show()


		self.qApp.exec_()



### PRIVATE ###



# -todo 88 (fix, gcode) +0: use dispatch both for file save
	def dispatchSend(self, _name):
		return self.dispatch.runDevice(_name, self.appWindow.dispatchLog)



	def storeWindow(self, _size, _maximized):
		self.args.set('wMaxi', _maximized)
		if not _maximized:
			self.args.set('wSize', (_size.width(),_size.height()) )



	def addFile(self):
		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		cMeta = self.data.loadXML(fileName, self.decorDefault)
		cXml = self.data.getXML()
		if cXml:
			self.appWindow.reactAddFile(cMeta, cXml)
		


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



#  todo 98 (module-ui, optimize) -1: prevent doubling by difference change
	def layerSetSelect(self, _selectionA):
		self.data.decorSet(self.decorSelect, _selectionA)

		self.reloadXml()



# -todo 77 (fix, module-ui, viewport) +0: duplicate hover element topmost
	def layerSetHover(self, _hover):
		self.data.decorSet(self.decorHover, [_hover] if _hover else [])

		self.reloadXml()



	def ctrlLayersSet(self, _elA, _on):
		self.data.decorSet(self.decorOff, _elA, not _on)


		self.reloadXml()



	def reloadXml(self):
		cXml = self.data.getXML()
		if cXml:
			self.appWindow.canvasUpdate(cXml)
