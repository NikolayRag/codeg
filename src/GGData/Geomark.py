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
#

class Geomark():
	allMarks___ = []


# =todo 127 (mark, optimize, decide) +10: Move marks assignment to Geoblock WTF?!
#  todo 126 (mark, optimize) +0: chage to {geo:state} dict
	assignedList___ = []
	updatedList___ = []



	def add___(_newMark):
		marksA = Geomark.allMarks___ + [_newMark]
		priorityList = set( [cMark.priority for cMark in marksA] )

		markSortedA = []

		for cLev in sorted(priorityList):
			for d in marksA:
				if d.priority==cLev:
					markSortedA.append(d)

		Geomark.allMarks___ = markSortedA



# Get {name:(mark,)} array, sorted by marks priority
	def getOrdered___(_namesLimit, _at):
		upNames = []

		for cMark in Geomark.allMarks___:
			if cMark.markFilter.step != _at:
				continue

			upNames += cMark.updatedList___

			cMark.resetAssigned___()


		outMark = {}

		for cName in set(upNames).intersection(_namesLimit):
			marksA = []
			updated = False

			for cMark in Geomark.allMarks___:
				if cName in cMark.assignedList___:
					marksA.append(cMark)

					updated = True

			if updated:
				outMark[cName] = marksA


		return outMark



### ###

# -todo 129 (mark) +0: store custom fields data list
	markData = None
	markFilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.markData = _data
		self.markFilter = _filter

		self.priority = _priority


		self.resetAssigned___(True)


		Geomark.add___(self)



	def resetAssigned___(self, _hard=False):
		self.updatedList___ = []

		if _hard:
			self.assignedList___ = []



	def assignGeo___(self, _namesA):
		_namesA = list(_namesA)

		self.updatedList___ += list( set(self.assignedList___).symmetric_difference(_namesA) )
		self.assignedList___ = _namesA



	def applyFilter(self, _geo):
		self.markFilter.proccess(_geo, self.markData)
