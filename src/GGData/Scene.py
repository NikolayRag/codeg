# =todo 9 (scene, spec, module-data) +1: operate project data
# =todo 113 (scene, module-ui, ux) +0: assignable layer marks holding control data
# =todo 93 (scene, feature) +0: store scene layer and layout state
#  todo 92 (feature) +0: multiple sources scene


from .Geomark import *
from .Geoblock import *



class Scene():
	allGeo = []
	allMarks = []


	def __init__(self):
		self.allGeo = []
		self.allMarks = []



### MARKS ###


# -todo 111 (mark, optimize) +0: dramatically slow apply
	def marksReapply___(self, _at):
		toMarksA = Geomark.getOrdered___(self.allGeo[0].names(), _at)
		for cName in toMarksA:
			for cMark in toMarksA[cName]:
				cMark.applyFilter(self.allGeo[0].getObj([cName])[0])



	def markAdd(self, _mark):
		self.allMarks.append( _mark )



	def markAppend(self, _mark, _elA):
		for cObj in self.allGeo[0].getObj(_elA):
			cObj.markAdd(_mark)



	def markRemove(self, _mark, _elA=None):
		for cObj in self.allGeo[0].getObj(_elA):
			cObj.markSub(_mark)



### GEO ###


	def geoAdd(self, _source, _type):
		self.allGeo.append( Geoblock(_source, _type) )

		return len(self.allGeo) -1



	def geoMeta(self):
		return {cN:{'on':True} for cN in self.allGeo[0].names()}



	def getSceneXML(self, toString=False):
		return self.allGeo[0].xmlRoot(toString)
