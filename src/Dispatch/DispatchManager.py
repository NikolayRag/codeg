
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



	def __init__(self, _definitions={}):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}


		self.allDevices = {}

#  todo 253 (module-dispatch, ux) +0: find all suitable devices
		for eName, eDef in _definitions.items():
			self.deviceDefine(eName, eDef[0], eDef[1], eDef[2])
		


	def deviceDefine(self, _name, _engine, _size, _definition=None):
		if _engine not in self.allEngines:
			print('Warning: engine', _engine, 'is unknown')

			return


		newDev = self.allEngines[_engine](_name, _size, _definition)
		self.allDevices[newDev.getName()] = newDev



	def deviceList(self):
		return dict(self.allDevices)
