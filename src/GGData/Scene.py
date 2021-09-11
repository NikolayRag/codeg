# =todo 9 (scene, spec, module-data) +1: operate project data
# =todo 113 (scene, module-ui, ux) +0: assignable layer decorator marks holding control data
# =todo 93 (scene, feature) +0: store scene layer and layout state
#  todo 92 (feature) +0: multiple sources scene




class Scene():
	geoList = None
	decList = None



	def __init__(self, _defDecs=[]):
		self.geoList = []
		self.decList = []


		for cDec in _defDecs:
			cDec.reset()

			self.decoratorAdd(cDec)



	def decoratorReapply(self):
		toDecorate = self.decoratorsOrder(self.geoList[0].names())
		for cName in toDecorate:
			for cDec in toDecorate[cName]:
				self.geoList[0].setTags(cName, cDec.tags)



	def decoratorAdd(self, _newDec):
		decList = self.decList + [_newDec]
		levels = sorted(set( [cDec.priority for cDec in decList] ))

		newDecSorted = []

		for cLev in levels:
			for d in decList:
				if d.priority==cLev:
					newDecSorted.append(d)

		self.decList = newDecSorted



# Get {name:(decorator,)} array, sorted by decorators priority
	def decoratorsOrder(self, _namesLimit):
		upNames = []

		for cDec in self.decList:
			upNames += cDec.updatedA

			cDec.cdown()


		outDec = {}

		for cName in set(upNames).intersection(_namesLimit):
			decList = []
			updated = False

			for cDec in self.decList:
				if cName in cDec.assigned:
					decList.append(cDec)

					updated = True

			if updated:
				outDec[cName] = decList


		return outDec


### GEO ###


	def geoAdd(self, _geo):
		self.geoList.append(_geo)

		return len(self.geoList) -1



	def geoMeta(self):
		return {cN:{'on':True} for cN in self.geoList[0].names()}



	def getSceneXML(self, toString=False):
		return self.geoList[0].xmlRoot(toString)
