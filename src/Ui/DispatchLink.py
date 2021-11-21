from threading import *


from PySide2.QtCore import *



'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink(QObject):
	sigDispatchSent = Signal(object)
	sigDeviceListed = Signal(list)


	dispatcher = None
	fallbackPlate = None



	def __init__(self, _fallbackPlate=(100,100), _dispatch=None):
		QObject.__init__(self)

		self.dispatcher = _dispatch
		self.fallbackPlate = _fallbackPlate



	def getDevices(self):
		if self.dispatcher:
			Thread(target=lambda: self.sigDeviceListed.emit(self.dispatcher.deviceList())).start()



# -todo 20 (module-dispatch, error ) +0: handle errors, maybe status string
#  todo 252 (module-dispatch, feature) +0: dispatch async
	def runDevice(self, _dev, _data):
		for cg in _data:
			self.dispatcher and self.dispatcher.deviceSend(_dev, cg)
			self.sigDispatchSent.emit(cg)



	def devicePlate(self, _dev):
		size = self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate
