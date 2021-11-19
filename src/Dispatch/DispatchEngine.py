class DispatchEngine():
	nameBase = ''
	name = ''

	sizeBase = (100,100)
	size = None

	privData = None

	instances = {}



	### OVERLOAD ###

	@classmethod
	def enumerate(it, _defSize=None):
		return it.instances



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