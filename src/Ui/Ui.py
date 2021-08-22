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
	cbFileLoad = None
	cbFileSave = None


	layerHover = None
	layersSelection = []



	def dispatchGetList(self):
		return self.dispatch.getDevices()



# =todo 88 (fix, gcode) +0: use dispatch both for file save
# =todo 87 (fix, gcode) +0: place svg layers more generally
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
		self.appWindow = AppWindow()

		self.appWindow.setCBResize(self.storeWindow)
		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.setCBFileLoad(self.openFile)
		self.appWindow.setCBFileSave(self.storeFile)
		self.appWindow.setCBLayerSet(self.layerSet)

		self.appWindow.setCBConnList(self.dispatchGetList)
		self.appWindow.setCBDispatch(self.dispatchSend)



	def go(self):
		self.appWindow.exec()



	def openFile(self):
		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		self.layerHover = None
		self.layersSelection = []

		return self.data.loadXML(fileName)
		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeFile(self):
		if not self.data.info():
			print("No scene data")
			return


		cRecentA = self.args.get("recentSaved", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(None, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		h = self.appWindow.layout.viewport.canvas.docHeight
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
