# -todo 22 (module-ui, ux) +0: make time consuming functions, like saveload, interruptable
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer




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


	def dispatchSend(self, _name):
		return self.dispatch.runDevice(_name)



	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch

		#init
		self.appWindow = AppWindow(self.args)


		self.appWindow.setCBFileLoad(self.openFile)
		self.appWindow.setCBFileSave(self.storeFile)
		self.appWindow.setCBLayerSet(self.layerSet)

		self.appWindow.setCBConnList(self.dispatchGetList)
		self.appWindow.setCBDispatch(self.dispatchSend)



	def go(self):
		self.appWindow.exec()



	def openFile(self):
		cRecentA = self.args.args["recentLoaded"] if ("recentLoaded" in self.args.args) else []

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.args["recentLoaded"] = cRecentA + [fileName]


		self.layerHover = None
		self.layersSelection = []

		return self.data.loadXML(fileName)
		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeFile(self):
		if not self.data.info():
			print("No scene data")
			return


		cRecentA = self.args.args["recentSaved"] if ("recentSaved" in self.args.args) else []

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(None, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		with open(fileName, 'w') as f:
			f.write(self.data.getG())


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.args["recentSaved"] = cRecentA + [fileName]




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

		self.data.override(self.layerHover, self.styleHover)


		return self.data.getXML()
