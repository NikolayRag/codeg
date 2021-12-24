from threading import *


from PySide2.QtCore import *



# -todo 261 (module-dispatch, feature) +1: add basic dispatch session management
# =todo 307 (device) +0: add device start/stop control routines
class DispatchSession(Thread, QObject):
	errOk = 1
	errDevice = 2
	errCancel = 3


	sigStart = Signal()
	sigFeed = Signal(object, tuple, str)
	sigFinish = Signal(int)


	gIn = []
	gOut = []


	_liveData = None



# -todo 300 (module-dispatch, device) +0: read device nonblocking from session
	def __init__(self, _cb, _data, gIn=[], gOut=[]):
		Thread.__init__(self)
		QObject.__init__(self)


		self.runCb = _cb
		bbox = _data['meta']
		self.runBox = [bbox[0], bbox[2], bbox[1]-bbox[0], bbox[3]-bbox[2]]
		self.runData = _data['data']
		self.gIn = gIn
		self.gOut = gOut

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



	def runBlock(self, _gBlock, _runtime):
		for cg in _gBlock:
			if _runtime:
				self.pauseEv.wait()
				if self.flagCancel:
					self.resultEnd = self.errCancel
					break


			res = self.runCb(cg)
			self.resultRuntime.append(res)

			if _runtime: self.sigFeed.emit(*res, cg)


			if res[0]!=True:
				self.resultEnd = self.errDevice
				return


		return True



	def run(self):
		self.pause(False)

		self.sigStart.emit()


		runState = self.runBlock(self.gIn, False)
		runState = runState and self.runBlock(self.runData, True)
		runState = runState and self.runBlock(self.gOut, False)


		if runState:
			res = self.runCb(None)
			self.resultRuntime.append(res)

			self.resultEnd = self.errOk if res[0]==True else self.errDevice


		self.sigFinish.emit(self.resultEnd)



	def liveData(self):
		return self._liveData



	def viewBox(self):
		return list(self.runBox)



	def pathLen(self):
		return len(self.runData)
