class DispatchEngine():
	size = None



	def __init__(self, _width, _height):
		self.size = (_width, _height)



	def getPlate(self):
		return self.size



	def sink(self, _data):
		return True