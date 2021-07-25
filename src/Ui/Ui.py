from .AppWindow import *


class Ui():
	args = None

	appWindow = None


	def __init__(self, _args):
		self.args = _args


		#init
		self.appWindow = AppWindow(self.args)


		self.appWindow.exec()


		logging.warning('Exiting')
		self.args.save()
