#  todo 15 (spec, module-ui, viewport) +0: basic mouse zoom, pan and reset
#  todo 16 (spec, module-ui) +0: layers

# =todo 22 (module-ui, ux) +0: make time consuming functions, like saveload, interruptable
# =todo 23 (module-ui, ux) +0: show progress for time consuming operations
# =todo 27 (module-ui, ux) +0: allow append gcode from text field (paste)




from .AppWindow import *


class Ui():
	args = None

	appWindow = None


	def __init__(self, _args):
		self.args = _args


		#init
		self.appWindow = AppWindow(self.args)


	
	def setUICB(self, _cbFL, _cbFS):
		self.appWindow.setCBFileLoad(_cbFL);
		self.appWindow.setCBFileSave(_cbFS);



	def go(self):
		self.appWindow.exec()


