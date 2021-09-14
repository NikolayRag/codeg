'''
Filter container class
Holds filter function, filter roadpoint and supply data to be applied
to object layer

Filter roadpoint is one of several known origins:
- at creation/load
- at user explicit action
- at output
'''



# =todo 112 (mark, feature) +0: complex mark
# =todo 124 (filter, module-data) +0: make set svg tag as system filter

class Geomark():

	FORNEW = 10
	FOREXPLICIT = 20
	FOROUT = 30

	filtersDict = None



	def __init__(self, _data, _priority=0, filters={}):
		self.priority = _priority
		self.assigned = []
		self.updatedA = []


		for cFilt in filters:
			if cFilt in (FORNEW, FOREXPLICIT, FOROUT):
				self.filtersDict = filters[cFilt]

		self.tags = _data



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

