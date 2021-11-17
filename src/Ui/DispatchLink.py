from PySide2.QtCore import *



# Interface for separate Dispatch
# Dispatch connected either inline, or as app link
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink(QObject):
	sigDispatchSent = Signal(object)


	dispatcher = None
	fallbackEng = {}



	def __init__(self, _fallbackEng, _dispatch=None):
		QObject.__init__(self)

		self.dispatcher = _dispatch
		self.fallbackEng = _fallbackEng



	def getDevices(self):
		devs = {self.fallbackEng.getName(): self.fallbackEng} if self.fallbackEng else {}

		if self.dispatcher:
			devs = {**devs, **self.dispatcher.deviceList()}

		return devs



# -todo 20 (module-dispatch, error ) +0: handle errors, maybe status string
#  todo 252 (module-dispatch, feature) +0: dispatch async
	def runDevice(self, _dev, _data):
		for cg in _data:
			_dev.sink(cg)
			self.sigDispatchSent.emit(cg)
