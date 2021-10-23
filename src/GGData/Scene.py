# =todo 11 (spec, module-data) +0: read/save scene data
#  todo 92 (feature) +0: multiple sources scene


from .Mark import *
from .Geoblock import *



class Scene():
	dirtyFlag = False

	allGeo = []
	allMarks = []

	name = ''


	def __init__(self, _name=''):
		self.dirtyFlag = False

		self.allGeo = []
		self.allMarks = []

		self.name = _name



	def packScene(self):
		out = {
			'name': self.name
		}


		markBlock = {}
		mId = 0
		for cMark in self.allMarks:
			markBlock[mId] = cMark.packMark()
			mId += 1

		out['markBlock'] = markBlock


		geoBlock = []
		
		for cGeo in self.allGeo:
			geoBlock.append( cGeo.packGeo(self.allMarks) )

		out['geoBlock'] = geoBlock


		return out


	def isDirty(self):
		for cMark in self.allMarks:
			if cMark.isDirty():
				return True


		for cGeo in self.allGeo:
			if cGeo.isDirty():
				return True


		return self.dirtyFlag



	def clean(self, _all=True):
		self.dirtyFlag = False

		if not _all:
			return


		for cMark in self.allMarks:
			cMark.clean()


		for cGeo in self.allGeo:
			cGeo.clean()



### MARKS ###


	def markAppend(self, _mark):
		if _mark in self.allMarks:
			return


		self.allMarks.append( _mark )


		self.dirtyFlag = True

		return True



	def markList(self):
		return list(self.allMarks)



	def markIn(self, _mark):
		return _mark in self.allMarks



	def markRemove(self, _mark):
		if _mark not in self.allMarks:
			return


		self.allMarks.remove( _mark )


		self.dirtyFlag = True

		return True


### GEO ###


#  todo 84 (module-data) +0: make file load plugin system
	def geoAdd(self, _source, _type='svg'):
		geo = Geoblock(_source, _type)
		self.allGeo.append( geo )


		self.dirtyFlag = True

		return geo



	def getSceneXML(self, toString=False):
		out = {}
		for cGeo in self.allGeo:
			out = cGeo.xmlRoot(toString)

		return out



	def getSceneObjs(self, _name):
		out = {}
		for cGeo in self.allGeo:
			out = cGeo.getObj(_name)

		return out
