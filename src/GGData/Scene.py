# =todo 11 (spec, module-data) +0: read/save scene data
#  todo 92 (feature) +0: multiple sources scene


from .Mark import *
from .Geoblock import *

from .GGen import *



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
	def geoAdd(self, _source, _marks=[], _solve=None):
		geo = Geoblock(_source)
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
	def getSceneXML(self, toString=False):
		out = {}
		for cGeo in self.allGeo:
			out = cGeo.xmlRoot(toString)

		return out




# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cScene = self.getSceneXML()
		if not cScene:
			return ''


		cGG = GGen(cScene)
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapePreHook(_element):
			refGeo = self.geoList()[0].getGeo([_element.get('id')])

			if not refGeo:
				return False

			if not refGeo[0].dataGet('visible', True):
				return False


			return 'G0'


		def shapeInHook(_element, _point):
			return( "S100 G1" )

		cGG.set(shapeIn=shapeInHook, shapePre=shapePreHook)


		gFlat = []
		for g in cGG.generate( xform=[[1,0,x], [0,-1,y]] ):
			gFlat += g

		return "\n".join(gFlat)

