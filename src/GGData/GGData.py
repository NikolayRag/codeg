# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

# =todo 134 (module-data, api) -1: Clean Scene and further classes to be used as a GGData API part

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
from .Geomark import *
from .Geofilter import *
from .Filters import *



class GGData():

	allFilters = {}
	allScenes = {}
	currentScene = 0



	def __init__(self):
		self.allFilters = {a.__name__:a for a in Geofilter.__subclasses__()}



	def sceneRemove(self, _id=-1):
		if _id == -1:
			self.allScenes = {}

			return


		del self.allScenes[_id]



	def sceneNew(self, focus=False):
		i = 0
		
		if self.allScenes:
			i = max(self.allScenes, key=int) +1

		self.allScenes[i] = Scene()


		if focus:
			self.sceneFocus(i)


		return i



	def sceneGet(self, _id=-1):
		if _id == -1:
			_id = self.currentScene


		return (_id in self.allScenes) and self.allScenes[_id]



	def sceneList(self):
		return dict(self.allScenes)



	def sceneFocus(self, _id=None):
		if _id != None:
			self.currentScene = _id


		return self.currentScene


###


	def markNew(self, data={}, filterName=None, filterData={}, priority=0):
		if filterName not in self.allFilters:
			print('Warning: filter', filterName, 'is unknown')

			newclass = type('Filter'+filterName, (Geofilter,),{"name": filterName})
			self.allFilters[filterName] = newclass


		filterProc = self.allFilters[filterName](filterData)


		cMark = Geomark(data, priority, filterProc)
		return cMark


###


# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.sceneGet():
			return

#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cGG = GGen(self.sceneGet().getSceneXML())
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapePreHook(_element):
			refGeo = self.sceneGet().getSceneObjs([_element.get('id')])

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


