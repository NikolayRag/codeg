#  todo 84 (module-data) +0: make file load plugin system

import os.path as path


from .Mark import *
from .Geoblock import *



class Scene():
	dirtyFlag = False

	geoNames = {}
	allGeo = []
	allMarks = []

	name = ''


	def geoNameUniq(self, _source, _name):
		_source = _source[:30]

		refName = path.basename(_source).split('.')[:-1]
		refName = '.'.join(refName)
		refCount = 0
		if refName in self.geoNames:
			refCount = self.geoNames[refName] +1


		if not _name:
			_name = f"{refName}({refCount})" if refCount>0 else refName

		self.geoNames[refName] = refCount

		return _name



	def __init__(self, _name=''):
		self.dirtyFlag = False

		self.geoNames = {}
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


	def geoAdd(self, _source, _marks=[], _solve=None, name=None, raw=False):
		geo = Geoblock(_source, self.geoNameUniq(_source, name), raw=raw)
		self.allGeo.append( geo )

		for cGeo in geo.getGeo():
			for cMark in _marks:
				cGeo.markSet(cMark, True)

			if _solve:
				cGeo.marksSolve(filterStep=_solve)


		self.dirtyFlag = True

		return geo



	def geoList(self):
		return list(self.allGeo)



	def traceG(self, _x=0, _y=0):
		data = []

		bbox = None
		for cObj in self.geoList():
			data += cObj.trace(_x, _y)

			cBox = cObj.bbox()
			bbox = bbox or cBox

			if bbox[0]>cBox[0]: bbox[0]=cBox[0]
			if bbox[1]<cBox[1]: bbox[1]=cBox[1]
			if bbox[2]>cBox[2]: bbox[2]=cBox[2]
			if bbox[3]<cBox[3]: bbox[3]=cBox[3]


		return {
			'meta': bbox or (0,1,0,1),
			'data': data
		}

