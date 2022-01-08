from threading import *


from PySide2.QtCore import *



'''
Dispatch session is g-data sending daemon.
It doesn't deal with Dispatcher or Device, and only use provided sink callback.
'''
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



# =todo 337 (module-dispatch, session) +0: add continuous session
# -todo 300 (module-dispatch, device) +0: read device nonblocking from session
	def __init__(self, _cb, _bbox, _data=[], gIn=[], gOut=[], live=False):
		Thread.__init__(self)
		QObject.__init__(self)


		self.runCb = _cb
		self.runBox = [_bbox[0], _bbox[2], _bbox[1]-_bbox[0], _bbox[3]-_bbox[2]]
		self.runDataQ = [_data]
		self.dataLen = len(_data)


		self.gIn = gIn
		self.gOut = gOut

		self.resultEnd = None
		self.resultRuntime = []

		self.pauseEv = Event()
		self.flagCancel = False

		self.isLive = live
		self.nodataEv = Event()


		self._liveData = type('', (object,), {})



#  todo 343 (clean) +0: join cancel() anf final()
	def cancel(self, _instant=False):
		self.final()


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
# =todo 330 (dispatch, device) +0: pause device using pause/unpause commands
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


		self.resultEnd = self.errOk
		runState = self.runBlock(self.gIn, False)

		while runState:
			if not self.runDataQ:
				if self.isLive:
					self.nodataEv.wait()
				
				if not self.isLive:
					break

			self.nodataEv.clear()


			runState = self.runBlock(self.runDataQ.pop(0), True)

		runState = runState and self.runBlock(self.gOut, False)


		if runState:
			res = self.runCb(None)
			self.resultRuntime.append(res)

			if res[0] != True:
				self.resultEnd = self.errDevice


		self.sigFinish.emit(self.resultEnd)



	def add(self, _data):
		self.runDataQ.append(_data)
		self.dataLen += len(_data)

		self.nodataEv.set()



	def final(self):
		self.isLive = False

		self.nodataEv.set()



	def liveData(self):
		return self._liveData



	def viewBox(self):
		return list(self.runBox)



	def pathLen(self):
		return self.dataLen
