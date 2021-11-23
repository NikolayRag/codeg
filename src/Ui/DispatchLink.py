from threading import *


from PySide2.QtCore import *



# =todo 261 (module-dispatch, feature) +0: add basic dispatch session manager
class DispatchSession(Thread, QObject):
	sigSent = Signal(object, object)
	sigFinish = Signal(bool)


	def __init__(self, _cb, _data):
		Thread.__init__(self)
		QObject.__init__(self)


		self.runCb = _cb
		self.runMeta = _data['meta']
		self.runData = _data['data']



	def run(self):

		for cg in self.runData:
			if not cg:
				continue

			res = self.runCb(cg)
			self.sigSent.emit(cg, res)

			if res==False:
				self.sigFinish.emit(False)

				return


		res = self.runCb(None)

		self.sigFinish.emit(bool(res))



	def viewBox(self):
		return list(self.runMeta)



	def pathLen(self):
		return len(self.runData)



'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
#  todo 258 (module-dispatch, error, ux) +0: handle retries
class DispatchLink(QObject):
	sigDeviceFound = Signal(str)
	sigDeviceListed = Signal(list)
	sigDispatchSent = Signal(object, object)
	sigDispatchFinish = Signal(bool)


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
			Thread(target=lambda: self.sigDeviceListed.emit(self.dispatcher.deviceList(self.sigDeviceFound.emit))).start()



# -todo 263 (module-dispatch, feature) +0: add dispatch queue
	def runDevice(self, _dev, _data):
		if not self.dispatcher:
			print ('No dispatcher')
			return

		def bindDev(_d):
			return self.dispatcher.deviceSend(_dev, _d)

		cSession = DispatchSession(bindDev, _data)
		cSession.sigFinish.connect(self.sigDispatchFinish)
		cSession.sigSent.connect(self.sigDispatchSent)

		cSession.start()

		self.allSessions.append(cSession)
		return cSession



	def devicePlate(self, _dev):
		size = self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate
