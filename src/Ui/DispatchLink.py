from threading import *


from PySide2.QtCore import *



'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink(QObject):
	sigDispatchSent = Signal(object)
	sigDispatchFinish = Signal(bool)
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



# =todo 252 (module-dispatch, feature) +0: dispatch async
#  todo 258 (module-dispatch, error, ux) +0: handle retries
	def runDevice(self, _dev, _data):
		if not self.dispatcher:
			print ('No dispatcher')
			return


		for cg in _data:
			if not cg:
				continue

			res = self.dispatcher.deviceSend(_dev, cg)
			self.sigDispatchSent.emit(f"+ {cg}" if res==True else f"  {res or 'Warning'}:\n- {cg}")

			if res==False:
				self.sigDispatchFinish.emit(False)

				return


		res = self.dispatcher.deviceSend(_dev, None)

		self.sigDispatchFinish.emit(bool(res))



	def devicePlate(self, _dev):
		size = self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate
