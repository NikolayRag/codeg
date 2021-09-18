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


	def marksReapply(self):
		toMark = self.marksOrder(self.geoList[0].names())
		for cName in toMark:
			for cMark in toMark[cName]:
				self.geoList[0].setTags(cName, cMark.tags)



	def markAdd(self, _newMark):
		marksA = self.markList + [_newMark]
		levels = sorted(set( [cMark.priority for cMark in marksA] ))

		markSortedA = []

		for cLev in levels:
			for d in marksA:
				if d.priority==cLev:
					markSortedA.append(d)

		self.markList = markSortedA



# Get {name:(mark,)} array, sorted by marks priority
	def marksOrder(self, _namesLimit):
		upNames = []

		for cMark in self.markList:
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
