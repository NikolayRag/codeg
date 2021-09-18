# =todo 9 (scene, spec, module-data) +1: operate project data
# =todo 113 (scene, module-ui, ux) +0: assignable layer marks holding control data
# =todo 93 (scene, feature) +0: store scene layer and layout state
#  todo 92 (feature) +0: multiple sources scene




class Scene():
	geoList = None
	markList = None



	def __init__(self, _defaultMarks=[]):
		self.geoList = []
		self.markList = []


		for cMark in _defaultMarks:
			cMark.reset(True)

			self.markAdd(cMark)


### MARKS ###


	def markAdd(self, _newMark):
		marksA = self.markList + [_newMark]
		levels = sorted(set( [cMark.priority for cMark in marksA] ))

		markSortedA = []

		for cLev in levels:
			for d in marksA:
				if d.priority==cLev:
					markSortedA.append(d)

		self.markList = markSortedA



# -todo 111 (mark, optimize) +0: dramatically slow apply
	def marksReapply(self, level=0):
		toMarksA = self.marksOrder(self.geoList[0].names(), level)
		for cName in toMarksA:
			for cMark in toMarksA[cName]:
				cMark.applyFilter(self.geoList[0].geo(cName))



# Get {name:(mark,)} array, sorted by marks priority
	def marksOrder(self, _namesLimit, _level):
		upNames = []

		for cMark in self.markList:
			if _level != cMark.markLevel:
				continue

			upNames += cMark.updatedList

			cMark.reset()


		outMark = {}

		for cName in set(upNames).intersection(_namesLimit):
			marksA = []
			updated = False

			for cMark in self.markList:
				if cName in cMark.assignedList:
					marksA.append(cMark)

					updated = True

			if updated:
				outMark[cName] = marksA


		return outMark


### GEO ###


	def geoAdd(self, _geo):
		self.geoList.append(_geo)

		return len(self.geoList) -1



	def geoMeta(self):
		return {cN:{'on':True} for cN in self.geoList[0].names()}



	def getSceneXML(self, toString=False):
		return self.geoList[0].xmlRoot(toString)
