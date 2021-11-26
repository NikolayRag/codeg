
# =todo 22 (module-dispatch, ux) +1: make dispatch interruptable
# =todo 61 (module-dispatch) +0: CNC control
# -todo 64 (module-dispatch) +0: dispatch queue
# -todo 68 (module-dispatch) +0: queue control
# =todo 165 (feature, dispatch) +0: device definition


'''
Dispatch Engines creation fabric and manager
'''

from threading import *


from .DispatchEngine import *
from .Engines import *



class EventAcc(Event):
	acc = 0


	def __init__(self):
		Event.__init__(self)

		self.acc = 0


	def inc(self, v=1):
		self.acc += v


	def dec(self, v=1):
		self.acc -= v
		if not self.acc:
			self.set()


	def waitAll(self, timeout=None):
		self.wait(timeout)




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
#  todo 266 (module-dispatch, test) +0: handle device rescan interfere case
	def deviceList(self, _cb=None):
		self.allDevices = {}

		evDone = EventAcc()


		def devOk(_dev, _ev):
			if _dev.test():
				_cb and _cb(_dev.getName(), True)

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



	def deviceSize(self, _dev):
		if _dev in self.allDevices:
			return self.allDevices[_dev].getPlate()



	def deviceSend(self, _dev, _data=None):
		if _dev in self.allDevices:
			res = self.allDevices[_dev].sink(_data)
			return res
