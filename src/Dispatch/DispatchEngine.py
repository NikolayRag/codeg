class DispatchEngine():
	size = None
	definition = None



	def __init__(self, _size, _def):
		self.size = _size
		self.definition = _def
		


	def getPlate(self):
		return self.size



	def sink(self, _data):
		return True