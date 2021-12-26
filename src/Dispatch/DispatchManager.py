# -todo 287 (test) +0: scan devices while busy


# -todo 61 (module-dispatch) +0: CNC manual control
# -todo 68 (module-dispatch) +0: queue control
# -todo 165 (feature, dispatch) +1: device settings definition


from threading import *


from .DispatchEngine import *
from .Engines import *


'''
Accumulated Event, triggered by internal accumulator reaching threshold, default 0.
Accumulator is changed with .inc(int=1) and .dec(int=1), inited with 0 by default.
.inc() and .dec() accept (test=bool) arg, telling to check trigger at the call, default to True.
'''
class EventAcc(Event):
	acc = 0
	thresh = 0


	def __init__(self, _acc=0):
		Event.__init__(self)

		self.acc = _acc


	def inc(self, v=1, test=True):
		self.acc += v
		if test and self.acc == self.thresh:
			self.set()


	def dec(self, v=1, test=True):
		self.acc -= v
		if test and self.acc == self.thresh:
			self.set()


	def waitAll(self, thresh=0, timeout=None):
		self.thresh = thresh
		self.wait(timeout)




'''
Dispatch Engines creation fabric and manager.
'''
class DispatchManager():

	allEngines = {}
	allDevices = {}


	defaultSize = ()
	definitions = {} #{engine: data}



	def __init__(self, size=(100,100), definitions={}):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}

		self.definitions = definitions
		self.defaultSize = size



	'''
	Enumerate and scan devices.
	_cb callback provided is called with valid device name when found

	Return {name: referenceId}
	'''
	def deviceList(self, _cb=None):
		self.allDevices = {}

		evDone = EventAcc()


		def devOk(_dev, _ev):
			if _dev.test():
				_cb and _cb(_dev.getName())

				self.allDevices[_dev.getName()]= _dev


			_ev.dec()


		for engN, cEng in self.allEngines.items():
			engDefs = self.definitions[engN] if engN in self.definitions else None
			devEnum = cEng.enumerate(engDefs)
			evDone.inc(len(devEnum))

			for devName, devData in devEnum.items():
				cDev = cEng(devName, privData=devData)
				cDev.defSize(self.defaultSize)

				Thread(target=lambda: devOk(cDev, evDone)).start()


		evDone.waitAll()

		return list(self.allDevices.keys())



	#  todo 284 (module-dispatch, clean) +0: add deviceMeta
	def deviceSize(self, _dev):
		if _dev in self.allDevices:
			return self.allDevices[_dev].getPlate()



#  todo 275 (module-dispatch, clean) +0: rescan device at stop state

	def deviceSend(self, _dev, _data=None):
		res = (False, [])

		if _dev in self.allDevices:
			res = self.allDevices[_dev].sink(_data)

			if res != True:
				self.allDevices[_dev].lastError(res)


		return res



	def deviceState(self, _dev):
		if _dev not in self.allDevices:
			return False

		return self.allDevices[_dev].lastError()
