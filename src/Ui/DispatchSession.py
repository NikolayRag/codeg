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
