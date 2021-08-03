#  todo 16 (module-ui, viewport) +0: layers

# -todo 22 (module-ui, ux) +0: make time consuming functions, like saveload, interruptable
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer




from .AppWindow import *


class Ui():
	args = None

	appWindow = None


	def __init__(self, _args):
		self.args = _args


		#init
		self.appWindow = AppWindow(self.args)


	
	def setUICB(self, _cbFL, _cbFS, _cbConnList, _cbDispatch):
		self.appWindow.setCBFileLoad(_cbFL);
		self.appWindow.setCBFileSave(_cbFS);
		self.appWindow.setCBConnList(_cbConnList);
		self.appWindow.setCBDispatch(_cbDispatch);



	def go(self):
		self.appWindow.exec()


