
# =todo 22 (module-dispatch, ux) +1: make dispatch interruptable
# -todo 60 (module-dispatch) +0: show gcodes live proto
# =todo 61 (module-dispatch) +0: CNC control
# -todo 62 (module-dispatch) +0: live device control
# -todo 64 (module-dispatch) +0: dispatch queue
# -todo 68 (module-dispatch) +0: queue control


'''
Dispatch Engines creation fabric

'''


from .DispatchEngine import *
from .Engines import *



class DispatchManager():
	allEngines = {}
	allDevices = {}



	def __init__(self, size=(100,100), definitions={}):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}

		self.allDevices = {}
		self.devicesScan(definitions)

		for cDev in self.allDevices.values():
			cDev.defSize(size)



# =todo 254 (module-dispatch, ux) +0: make devices async
	def devicesScan(self, _definitions):
		for engN, cEng in self.allEngines.items():
			engDefs = _definitions[engN] if engN in _definitions else None
			for cDev in cEng.enumerate(engDefs):
				self.allDevices[cDev.getName()]= cDev



	def deviceList(self):
		return dict(self.allDevices)
