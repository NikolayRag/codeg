from .AppWindow import *


class Ui():
	args = None

	appWindow = None


	def __init__(self, _args):
		self.args = _args


		#init
		self.appWindow = AppWindow()


		self.appWindow.exec()

