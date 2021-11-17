class DispatchEngine():
	name = 'Dummy'

	size = None
	definition = None



	def __init__(self, _name, _size, _definition=None):
		self.name = _name
		self.size = _size
		self.definition = _definition



	def getPlate(self):
		return self.size



	def getName(self):
		return self.name



	def sink(self, _data):
		return True