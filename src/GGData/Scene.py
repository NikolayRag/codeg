# =todo 11 (spec, module-data) +0: read/save scene data
# =todo 9 (scene, spec, module-data) +1: operate project data
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


	def markAppend(self, _mark):
		self.allMarks.append( _mark )



	def markList(self):
		return list(self.allMarks)



# -todo 111 (mark, optimize) +0: dramatically slow mark reapply
	def markGeoAdd(self, _mark, _elA):
		for cObj in self.allGeo[0].getObj(_elA):
			cObj.markAdd(_mark)



	def markGeoSub(self, _mark, _elA=None):
		for cObj in self.allGeo[0].getObj(_elA):
			cObj.markSub(_mark)



	# part: True/False/None points to add/sub/reset
	def markApply(self, _mark, _elA, part=None, step=None):
		if part==True:
			self.markGeoAdd(_mark, _elA)

		if part==False:
			self.markGeoSub(_mark, _elA)

		if part==None:
			self.markGeoSub(_mark)
			if _elA:
				self.markGeoAdd(_mark, _elA)


		for cObj in self.allGeo[0].getObj():
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
