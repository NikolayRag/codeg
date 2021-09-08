# =todo 9 (scene, spec, module-data) +1: operate project data
# =todo 113 (scene, module-ui, ux) +0: assignable layer decorator marks holding control data
# =todo 93 (scene, feature) +0: store scene layer and layout state
#  todo 92 (feature) +0: multiple sources scene



class Scene():
	decorators = None



	def __init__(self, _defDecs=[]):
		self.decorators = []


		for cDec in _defDecs:
			cDec.reset()

			self.decoratorAdd(cDec)



	def decoratorAdd(self, _newDec):
		decList = self.decorators + [_newDec]
		levels = sorted(set( [cDec.priority for cDec in decList] ))

		newDecSorted = []

		for cLev in levels:
			for d in decList:
				if d.priority==cLev:
					newDecSorted.append(d)

		self.decorators = newDecSorted



# Get {name:(decorator,)} array, sorted by decorators priority
	def decoratorsOrder(self, _names):
		upNames = []

		for cDec in self.decorators:
			upNames += cDec.updatedA

			cDec.cdown()


		outDec = {}

		for cName in set(upNames).intersection(_names):
			decList = []
			updated = False

			for cDec in self.decorators:
				if cName in cDec.assigned:
					decList.append(cDec)

					updated = True

			if updated:
				outDec[cName] = decList


		return outDec
