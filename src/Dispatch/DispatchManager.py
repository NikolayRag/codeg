
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



	def __init__(self, _defs={}):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}


		self.allDevices = {}

		for eName, eDef in _defs.items():
			self.deviceDefine(eName, eDef[0], eDef[1])
		


	def deviceDefine(self, _name, _eName, _def=None):
		if _eName not in self.allEngines:
			print('Warning: engine', _eName, 'is unknown')

			return


		self.allDevices[_name] = self.allEngines[_eName](_def)



	def deviceList(self):
		return dict(self.allDevices)
