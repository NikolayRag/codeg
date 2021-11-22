from threading import *


from PySide2.QtCore import *



class DispatchSession(Thread, QObject):
	sigSent = Signal(object)
	sigFinish = Signal(bool)


	def __init__(self, _cb, _data):
		Thread.__init__(self)
		QObject.__init__(self)

		self.runCb = _cb
		self.runData = _data



	def run(self):

		dI = 0
		for cg in self.runData:
			dI += 1
			if not cg:
				continue

			res = self.runCb(cg)
			self.sigSent.emit(f"+ {cg}" if res==True else f"  {res or 'Warning'}:\n- {cg}")

			if res==False:
				self.sigFinish.emit(False)

				return


		res = self.runCb(None)

		self.sigFinish.emit(bool(res))




'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink(QObject):
	sigDispatchFire = Signal(object)
	sigDispatchSent = Signal(object)
	sigDispatchFinish = Signal(bool)
	sigDeviceListed = Signal(list)


	dispatcher = None
	fallbackPlate = None


	#runtime

	allSessions = []



	def __init__(self, _fallbackPlate=(100,100), _dispatch=None):
		QObject.__init__(self)

		self.dispatcher = _dispatch
		self.fallbackPlate = _fallbackPlate


		self.allSessions = []



	def getDevices(self):
		if self.dispatcher:
			Thread(target=lambda: self.sigDeviceListed.emit(self.dispatcher.deviceList())).start()



# =todo 252 (module-dispatch, feature) +0: dispatch async
#  todo 258 (module-dispatch, error, ux) +0: handle retries
	def runDevice(self, _dev, _data):
		if not self.dispatcher:
			print ('No dispatcher')
			return


		def bindDev(_data):
			return self.dispatcher.deviceSend(_dev, _data)

		cSession = DispatchSession(bindDev, _data)
		cSession.sigFinish.connect(self.sigDispatchFinish)
		cSession.sigSent.connect(self.sigDispatchSent)

		cSession.start()

		self.allSessions.append(cSession)
		self.sigDispatchFire.emit(cSession)



	def devicePlate(self, _dev):
		size = self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate
