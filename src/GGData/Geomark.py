'''
Geometry applied set of data
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
	allMarks = []


	markData = None
	markFilter = None
	markAt = 0
	priority = 0

#  todo 126 (mark, optimize) +0: chage to {geo:state} dict
	assignedList = []
	updatedList = []



	def add(_newMark):
		marksA = Geomark.allMarks + [_newMark]
		levels = sorted(set( [cMark.priority for cMark in marksA] ))

		markSortedA = []

		for cLev in levels:
			for d in marksA:
				if d.priority==cLev:
					markSortedA.append(d)

		Geomark.allMarks = markSortedA


		
# Get {name:(mark,)} array, sorted by marks priority
	def getOrdered(_namesLimit, _at):
		upNames = []

		for cMark in Geomark.allMarks:
			if _at != cMark.markAt:
				continue

			upNames += cMark.updatedList

			cMark.reset()


		outMark = {}

		for cName in set(upNames).intersection(_namesLimit):
			marksA = []
			updated = False

			for cMark in Geomark.allMarks:
				if cName in cMark.assignedList:
					marksA.append(cMark)

					updated = True

			if updated:
				outMark[cName] = marksA


		return outMark



	def __init__(self, _data, _priority=0, _filter=None, _at=None):
		self.markData = _data
		self.markFilter = _filter
		self.markAt = _at

		self.priority = _priority


		self.reset(True)


		Geomark.add(self)



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
