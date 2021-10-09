# =todo 11 (spec, module-data) +0: read/save scene data
# =todo 9 (scene, spec, module-data) +1: operate project data
#  todo 92 (feature) +0: multiple sources scene


from .Mark import *
from .Geoblock import *



class Scene():
	allGeo = []
	allMarks = []


	def __init__(self):
		self.allGeo = []
		self.allMarks = []



### MARKS ###


	def markAppend(self, _mark):
		if _mark in self.allMarks:
			return


		self.allMarks.append( _mark )

		return True



	def markList(self):
		return list(self.allMarks)



	def markRemove(self, _mark):
		if _mark not in self.allMarks:
			return

		
		self.allMarks.remove( _mark )

		return True



# -todo 111 (mark, optimize) +0: dramatically slow mark reapply

#  todo 139 (clean) +0: Clean mark to object appending
	# mode: True/False/None(default) for add/sub/set
	def markApplyGeo(self, _mark, _elA, mode=None, step=None):
		elSub = elAdd = self.allGeo[0].getObj(_elA)


		if mode==True:
			elSub = []

		if mode==False:
			elAdd = []

		if mode==None:
			elSub = self.allGeo[0].getObj()


		elAll = []

		for cObj in elSub:
			if cObj.markSub(_mark):
				elAll.append(cObj)

		for cObj in elAdd:
			if cObj.markAdd(_mark) and (cObj not in elAll):
				elAll.append(cObj)


		for cObj in elAll:
			cObj.marksSolve(filterStep=step)



### GEO ###


#  todo 84 (module-data) +0: make file load plugin system
	def geoAdd(self, _source, _type='svg'):
		self.allGeo.append( Geoblock(_source, _type) )

		return len(self.allGeo) -1



	def geoMeta(self):
		return {cN:{'on':True} for cN in self.allGeo[0].names()}



	def getSceneXML(self, toString=False):
		return self.allGeo[0].xmlRoot(toString)



	def getSceneObjs(self, _name):
		return self.allGeo[0].getObj(_name)



	def geoDataSet(self, _elA, _data):
		for cEl in _elA:
			self.allGeo[0].dataSet(cEl, _data)
