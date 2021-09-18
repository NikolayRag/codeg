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
	markData = None
	markFilter = None


	markLevel = 0
	priority = 0

	assignedList = []
	updatedList = []


	def __init__(self, _data, _priority=0, _filter=None):
		self.markData = _data
		self.priority = _priority
		self.reset(True)


		self.markFilter = _filter



	def reset(self, _hard=False):
		self.updatedList = []

		if _hard:
			self.assignedList = []



	def assignGeo(self, _namesA):
		_namesA = list(_namesA)

		self.updatedList += list( set(self.assignedList).symmetric_difference(_namesA) )
		self.assignedList = _namesA



	def applyFilter(self, _geo):
		self.markFilter.proccess(_geo, self.markData)
