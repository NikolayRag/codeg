# SVG tags override class
#  todo 109 (decorator, optimize) +0: too weird entire Decorator flow
class Decorator():
	decorators = []


#Decorators sorted by priority ascending
	def sort():
		levels = sorted(set( [cDec.priority for cDec in Decorator.decorators] ))

		newDec = []

		for cLev in levels:
			for d in Decorator.decorators:
				if d.priority==cLev:
					newDec.append(d)

		Decorator.decorators = newDec



	def __init__(self, _tags, _priority=0):
		self.tags = _tags
		self.priority = _priority
		self.assigned = []
		self.updatedA = []

		Decorator.decorators.append(self)
		Decorator.sort()



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



# Get {name:(decorator,)} array, sorted by decorators priority
	def order(_names, all=False):
		upNames = []

		for cDec in Decorator.decorators:
			upNames += cDec.updatedA

			cDec.cdown()


		outDec = {}

		for cName in set(upNames).intersection(_names):
			decList = []
			updated = False

			for cDec in Decorator.decorators:
				if cName in cDec.assigned:
					decList.append(cDec)

					updated = True

			if updated:
				outDec[cName] = decList


		return outDec
