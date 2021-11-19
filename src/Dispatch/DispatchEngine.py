class DispatchEngine():
	nameBase = ''
	name = ''

	sizeBase = None
	size = None

	privData = None



	def __init__(self, _name, _size, _privData=None):
		self.nameBase = _name
		self.sizeBase = _size
		self.privData = _privData



	def getPlate(self):
		return self.size or self.sizeBase



	def getName(self):
		return self.name or self.nameBase



	def sink(self, _data):
		return True