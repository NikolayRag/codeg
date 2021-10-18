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



	def collect(self):
		print('--------')
		print('SCENE', self.name)

		for cMark in self.allMarks:
			print(cMark)
			cMark.collect()


		for cGeo in self.allGeo:
			print(cGeo)
			cGeo.collect(self.allMarks)



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



	def markRemove(self, _mark):
		if _mark not in self.allMarks:
			return


		self.allMarks.remove( _mark )


		self.dirtyFlag = True

		return True



# -todo 111 (mark, optimize) +0: dramatically slow mark reapply

#  todo 139 (clean) +0: Clean mark to object appending
	# mode: True/False/None(default) for add/sub/set
	def markApplyGeo(self, _mark, _elA, mode=None, step=None):
		if not len(self.allGeo):
			return


		elSub = elAdd = self.allGeo[0].getObj(_elA)


		if mode==True:
			elSub = []

		if mode==False:
			elAdd = []

		if mode==None:
			elSub = self.allGeo[0].getObj()


		elAll = []

		for cObj in elSub:
			if cObj.markSub(_mark, _mark in self.allMarks):
				elAll.append(cObj)

		for cObj in elAdd:
			if cObj.markAdd(_mark, _mark in self.allMarks) and (cObj not in elAll):
				elAll.append(cObj)


		for cObj in elAll:
			cObj.marksSolve(filterStep=step)



### GEO ###


#  todo 84 (module-data) +0: make file load plugin system
	def geoAdd(self, _source, _type='svg'):
		self.allGeo.append( Geoblock(_source, _type) )


		self.dirtyFlag = True

		return len(self.allGeo) -1



	def geoMeta(self):
		out = {}
		for cGeo in self.allGeo:
			out = {cN:{'on':True} for cN in cGeo.names()}

		return out



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



	def geoDataSet(self, _elA, _data):
		for cEl in _elA:
			self.allGeo[0].dataSet(cEl, _data)
