
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
	def __init__(self):
		self.allEngines = {a.__name__:a for a in DispatchEngine.__subclasses__()}



	def getDevices(self):
		return dict(self.allDevices)
