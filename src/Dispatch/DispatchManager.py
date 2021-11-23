
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



class DispatchManager():

	allEngines = {}
	allDevices = {}


	definitions = {} #{engine: data}



	def __init__(self, size=(100,100), definitions={}):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}

		self.definitions = definitions
		self.defaultSize = size



# =todo 254 (module-dispatch, ux) +0: scan devices parallel
	def devicesScan(self, _cb=None):
		evDone = Event()
		evDone.count = 0


		def devOk(_dev, _ev):
			if _dev.test():
				_cb and _cb(_dev.getName())

				self.allDevices[_dev.getName()]= _dev


			_ev.count -= 1
			if not _ev.count:
				_ev.set()


		for engN, cEng in self.allEngines.items():
			engDefs = self.definitions[engN] if engN in self.definitions else None
			devEnum = cEng.enumerate(engDefs)
			evDone.count += len(devEnum)

			for devName, devData in devEnum.items():
				cDev = cEng(devName, privData=devData)
				cDev.defSize(self.defaultSize)

				Thread(target=lambda: devOk(cDev, evDone)).start()


		evDone.wait()



	'''
	Return {name: referenceId}
	'''
	def deviceList(self, _cb=None):
		self.allDevices = {}

		self.devicesScan(_cb)

		return list(self.allDevices.keys())



	def deviceSize(self, _dev):
		if _dev in self.allDevices:
			return self.allDevices[_dev].getPlate()



	def deviceSend(self, _dev, _data=None):
		if _dev in self.allDevices:
			res = self.allDevices[_dev].sink(_data)
			return res
