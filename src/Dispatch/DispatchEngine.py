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



	def __init__(self, _name, _size=None, _privData=None):
		self.nameBase = _name
		if _size:
			self.sizeBase = _size
		self.privData = _privData



	def getPlate(self):
		return self.size or self.sizeBase



	def getName(self):
		return self.name or self.nameBase



	def sink(self, _data):
		return True