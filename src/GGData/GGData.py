# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode


'''
Data scope:
	(Filter,)
	(Scene,)
		(Mark,)
			*Filter link
		(Geoblock,)/(Geo,)
			*Mark link

'''


from .GGen import *
from .Scene import *
from .Mark import *
from .Markfilter import *
from .Filters import *



class GGData():

	allFilters = {}
	allScenes = {}
	currentSceneId = 0

	maxMarkPriority = 0


	def __init__(self):
		self.allFilters = {a.__name__:a for a in Markfilter.__subclasses__()}



	def sceneRemove(self, _name):
		if _name in self.allScenes:
			del self.allScenes[_name]



	def sceneGet(self, _name=''):
		if _name not in self.allScenes:
			self.allScenes[_name] = Scene(_name)

		return self.allScenes[_name]



	def sceneList(self):
		return dict(self.allScenes)



###


#	Only create Mark with given Markfilter and data.
#	Should be appended to scene explicitely by Scene.markAppend().
	def markNew(self, data={}, filterName=None, filterData={}, priority=None):
		if priority==None:
			priority = self.maxMarkPriority +1

		self.maxMarkPriority = priority


		filterProc = None

		if filterName:
			if filterName not in self.allFilters:
				print('Warning: filter', filterName, 'is unknown')

				newclass = type('Filter'+filterName, (Markfilter,),{"name": filterName})
				self.allFilters[filterName] = newclass


			filterProc = self.allFilters[filterName](filterData)


		cMark = Mark(data, priority, filterProc)
		return cMark


###


# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, _scene, x=0, y=0):
#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cGG = GGen(_scene.getSceneXML())
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapePreHook(_element):
			refGeo = _scene.getSceneObjs([_element.get('id')])

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


