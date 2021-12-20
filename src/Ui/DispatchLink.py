from threading import *


from PySide2.QtCore import *



# -todo 261 (module-dispatch, feature) +1: add basic dispatch session manager
# -todo 307 (device) +0: add device critical stop routine
#  todo 268 (module-dispatch, feature) +0: handle concurent sessions
class DispatchSession(Thread, QObject):
	errOk = 1
	errDevice = 2
	errCancel = 3


	sigStart = Signal()
	sigFeed = Signal(object, tuple, str)
	sigFinish = Signal(int)


	_liveData = None



# -todo 300 (module-dispatch, device) +0: read device nonblocking from session
	def __init__(self, _cb, _data):
		Thread.__init__(self)
		QObject.__init__(self)


		self.runCb = _cb
		bbox = _data['meta']
		self.runBox = [bbox[0], bbox[2], bbox[1]-bbox[0], bbox[3]-bbox[2]]
		self.runData = _data['data']

		self.resultEnd = None
		self.resultRuntime = []

		self.pauseEv = Event()
		self.flagCancel = False


		self._liveData = type('', (object,), {})



	def cancel(self, _instant=False):
		self.flagCancel = True

		if _instant:
			self.runCb(False)

		self.pauseEv.set()



	def pause(self, _state=None):
		if _state==None:
			return not self.pauseEv.is_set()


		if self.flagCancel:
			return
		
		self.pauseEv.clear() if _state else self.pauseEv.set()



	def run(self):
		self.pause(False)

		self.sigStart.emit()


		for cg in self.runData:
			if not cg:
				continue

			self.pauseEv.wait()
			if self.flagCancel:
				break


			res = self.runCb(cg)
			self.resultRuntime.append(res)
			self.sigFeed.emit(*res, cg)

#  todo 275 (module-dispatch, clean) +0: rescan device at stop state
			if res[0]!=True:
				self.resultEnd = self.errDevice

				self.sigFinish.emit(self.resultEnd)
				return


		res = self.runCb(None)
		self.resultRuntime.append(res)
		self.sigFeed.emit(*res, '')

		self.resultEnd = self.errOk if res[0]==True else self.errDevice
		self.sigFinish.emit(self.resultEnd)



	def liveData(self):
		return self._liveData



	def viewBox(self):
		return list(self.runBox)



	def pathLen(self):
		return len(self.runData)



'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''
#  todo 18 (API, module-dispatch, v2) +0: standalone dispatcher over *cloud*
#  todo 258 (module-dispatch, error, ux) +0: handle retries
class DispatchLink(QObject):
	sigDeviceFound = Signal(str)
	sigDispatchAdded = Signal(object)


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
			Thread(target=lambda: self.dispatcher.deviceList(self.sigDeviceFound.emit)).start()



	def sessionIgnite(self):
		if self.allSessions:
			self.allSessions[0].start()



	def sessionFinish(self, _session, _res):
		if self.allSessions[0] == _session:
			self.allSessions = self.allSessions[1:]

			self.sessionIgnite()

		else:
			print('Dispatch out of order')



	def sessionStart(self, _dev, _data):
		if not self.dispatcher:
			print ('No dispatcher')
			return

		def bindDev(_d):
			return self.dispatcher.deviceSend(_dev, _d)

		cSession = DispatchSession(bindDev, _data)
		cSession.sigFinish.connect(lambda res: self.sessionFinish(cSession, res))

		self.allSessions.append(cSession)
		self.sigDispatchAdded.emit(cSession)
		if len(self.allSessions)==1:
			self.sessionIgnite()

		return cSession



	def devicePlate(self, _dev=None):
		size = _dev and self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate
