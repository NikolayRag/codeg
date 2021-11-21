class DispatchEngine():
	nameBase = ''
	name = ''

	sizeBase = (100,100)
	size = None

	privData = None



	### OVERLOAD ###

	#_defs format is variant and specific to engine
	def enumerate(it, _defs=None):
		return []



	def __init__(self, _name, privData=None):
		self.nameBase = _name
		self.privData = privData



	def defSize(self, _size):
		self.sizeBase = _size



	def getPlate(self):
		return self.size or self.sizeBase



	def getName(self):
		return self.name or self.nameBase



	'''
	Override: actually recieve data, None to finish session.

	Return True for no errors, False for critical, any other for warning
	'''
	def sink(self, _data=None):
		return True
