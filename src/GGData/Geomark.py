# Scene element marks class

class Geomark():

	def __init__(self, _tags, _priority=0):
		self.tags = _tags
		self.priority = _priority
		self.assigned = []
		self.updatedA = []



	def reset(self):
		self.assigned = []
		self.updatedA = []



	def assign(self, _namesA):
		self.wup( list(_namesA) )



	def add(self, _namesA):
		self.wup( list(set(self.assigned + _namesA)) )



	def sub(self, _namesA):
		self.wup( list(set(self.assigned).difference(_namesA)) )



	def wup(self, _namesA):
		self.updatedA += list( set(self.assigned).symmetric_difference(_namesA) )
		self.assigned = _namesA



	def cdown(self):
		self.updatedA = []

