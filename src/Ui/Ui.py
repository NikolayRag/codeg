#  todo 16 (module-ui, viewport) +0: layers

# -todo 22 (module-ui, ux) +0: make time consuming functions, like saveload, interruptable
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer




from .AppWindow import *


class Ui():
	args = None

	appWindow = None

	data = None
	cbFileLoad = None
	cbFileSave = None



	def __init__(self, _args, _data):
		self.args = _args

		self.data = _data

		#init
		self.appWindow = AppWindow(self.args)


	
	def setUICB(self, _cbConnList, _cbDispatch):
		self.appWindow.setCBFileLoad(self.openFile);
		self.appWindow.setCBFileSave(self.storeFile);
		self.appWindow.setCBLayerPick(self.layerPick);
		self.appWindow.setCBConnList(_cbConnList);
		self.appWindow.setCBDispatch(_cbDispatch);



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



	def layerPick(self, _name, _state):
		self.data.highlight(_name, _state)

		return self.data.xml()
