#  todo 303 (module-dispatch, API, clean) +0: clean up DeviceEngine property methods

'''
Root CNC device class
'''
class DispatchEngine():
	errPort = -1
	

	nameBase = ''
	name = ''

	sizeBase = (100,100)
	size = None

	privData = None



	def __init__(self, _name, privData=None):
		self.nameBase = _name
		self.privData = privData



	def defSize(self, _size):
		self.sizeBase = _size



	def getPlate(self):
		return self.size or self.sizeBase



	def getName(self):
		return self.name or self.nameBase



	### OVERLOAD ###

	'''
	Return {name: privData, ...} devices definition list to be inited later.
	_defs format is variant and specific to engine.
	'''
	def enumerate(it, _defs=None):
		return {}



	'''
	Actually recieve data, None to finish session.

	Return (True|errorcode, [echo]) where errorcode=0 stands for timeout
	'''
#  todo 270 (module-dispatch, clean) +0: add device queue control
	def sink(self, _data=None):
		return (True,None)



	'''
	Return True if object is valid device.
	'''
	def test(self):
		return False
