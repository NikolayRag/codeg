
# =todo 22 (module-dispatch, ux) +1: make dispatch interruptable
# =todo 61 (module-dispatch) +0: CNC control
# -todo 64 (module-dispatch) +0: dispatch queue
# -todo 68 (module-dispatch) +0: queue control
# =todo 165 (feature, dispatch) +0: device definition


'''
Dispatch Engines creation fabric and manager
'''


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
	def devicesScan(self):
		for engN, cEng in self.allEngines.items():
			engDefs = self.definitions[engN] if engN in self.definitions else None
			for devName, devData in cEng.enumerate(engDefs).items():
				cDev = cEng(devName, privData=devData)
				print('try', cDev.getName())
				if cDev.test():
					print('ok')
					self.allDevices[cDev.getName()]= cDev
					cDev.defSize(self.defaultSize)



	'''
	Return {name: referenceId}
	'''
	def deviceList(self):
		self.allDevices = {}

		self.devicesScan()

		return list(self.allDevices.keys())



	def deviceSize(self, _dev):
		if _dev in self.allDevices:
			return self.allDevices[_dev].getPlate()



	def deviceSend(self, _dev, _data=None):
		if _dev in self.allDevices:
			res = self.allDevices[_dev].sink(_data)
			return res
