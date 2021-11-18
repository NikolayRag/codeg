class DispatchEngine():
	nameBase = ''
	name = ''

	sizeBase = None
	size = None

	definition = None



	def __init__(self, _name, _size, _definition=None):
		self.nameBase = _name
		self.sizeBase = _size
		self.definition = _definition



	def getPlate(self):
		return self.size or self.sizeBase



	def getName(self):
		return self.name or self.nameBase



	def sink(self, _data):
		return True