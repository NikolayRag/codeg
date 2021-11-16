from PySide2.QtCore import *



class EngineNull():
	size = None



	def __init__(self, _width, _height):
		self.size = (_width, _height)



	def getPlate(self):
		return self.size




# Interface for separate Dispatch
# Dispatch connected either inline, or as app link
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink(QObject):
	sigDispatchSent = Signal(object)


	dispatcher = None
	defaults = {}



	def __init__(self, _defaults, _dispatch=None):
		QObject.__init__(self)

		self.dispatcher = _dispatch
		self.defaults = _defaults



	def getDevices(self):
		devs = {}
		for devN, devDim in self.defaults.items():
			devs[devN] = EngineNull(*devDim)


		if self.dispatcher:
			devs = {**devs, **self.dispatcher.getDevices()}

		return devs



# -todo 20 (module-dispatch, error ) +0: handle errors, maybe status string
#  todo 252 (module-dispatch, feature) +0: dispatch async
	def runDevice(self, _dev, _data):
		for cg in _data:
			self.sigDispatchSent.emit(cg)
