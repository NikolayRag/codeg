#  todo 84 (module-data) +0: make file load plugin system

import os.path as path


from .Mark import *
from .Geoblock import *

from .GGen import *



class Scene():
	dirtyFlag = False

	geoNames = {}
	allGeo = []
	allMarks = []

	name = ''


	def geoNameUniq(self, _source, _name):
		refName = path.basename(_source).split('.')[0]
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


	def geoAdd(self, _source, _marks=[], _solve=None, name=None):
		geo = Geoblock(_source, self.geoNameUniq(_source, name))
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



# =todo 205 (fix, module-data) +0: check for multiobject case

# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cObj = self.geoList()[0]
		cScene = cObj.xmlRoot(False)


		cGG = GGen(cScene)
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapePreHook(_element):
			refGeo = cObj.getGeo([_element.get('id')])

			if not refGeo:
				return False

			if not refGeo[0].dataGet('visible', True):
				return False


			return 'G0'


		def shapeInHook(_element, _point):
			refGeo = cObj.getGeo([_element.get('id')])
			cycle = refGeo[0].dataGet('Laser Cycle', 100)
			return( f"S{int(cycle)} G1" )

		cGG.set(shapeIn=shapeInHook, shapePre=shapePreHook)



		xf = cObj.xformSet()[2]

		gFlat = []
		for g in cGG.generate( xform=[[1,0,xf[0]+_x], [0,-1,-xf[1]+_y]] ):
			gFlat += g

		return "\n".join(gFlat)

