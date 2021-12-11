class DispatchEngine():
	errUnknown = -1
	errHW = -2
	

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

	Return True for no errors, False for critical, any other for warning
	'''
#  todo 270 (module-dispatch, clean) +0: add device queue control
	def sink(self, _data=None):
		return True



	'''
	Return True if object is valid device.
	'''
	def test(self):
		return False
