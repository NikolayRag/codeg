from .AppWindow import *


class Ui():
	args = None

	appWindow = None


	def __init__(self, _args):
		self.args = _args


		#init
		self.appWindow = AppWindow(self.args)


	
	def setUICB(self, _cbFL):
		self.appWindow.setCBFileLoad(_cbFL);



	def go(self):
		self.appWindow.exec()


