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



	def __init__(self):
		self.allFilters = {a.__name__:a for a in Geofilter.__subclasses__()}



#  todo 137 (module-data, scene) +0: multiscene
	def sceneClear(self, _id=-1):
		if _id == -1:
			self.allScenes = {}

			return


		del self.allScenes[_id]



	def sceneNew(self):
		i = 0
		
		if self.allScenes:
			i = max(self.allScenes, key=int) +1

		self.allScenes[i] = Scene()



	def getScene(self, _id=0):
		return self.allScenes and self.allScenes[_id]



	def getScenes(self, _id=0):
		return dict(self.allScenes)



# -todo 84 (module-data) +0: make file load plugin system
	def loadGeo(self, _source, _type='svg'):
		self.getScene().geoAdd(_source, _type)

		return self.getScene().geoMeta()



	def getXML(self):
		return (self.getScene() and self.getScene().getSceneXML(True))



	def available(self):
		return bool(self.getScene())



# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.getScene():
			return

#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cGG = GGen(self.getScene().getSceneXML())
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapePreHook(_element):
			refGeo = self.getScene().getSceneObjs([_element.get('id')])

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



	def markNew(self, data={}, filterName=None, filterData={}, priority=0, scene=False):
		if filterName not in self.allFilters:
			print('Warning: filter', filterName, 'is unknown')

			newclass = type('Filter'+filterName, (Geofilter,),{"name": filterName})
			self.allFilters[filterName] = newclass


		filterProc = self.allFilters[filterName](filterData)


		cMark = Geomark(data, priority, filterProc)
		if scene and self.getScene():
			self.getScene().markAppend(cMark)

		return cMark



	# part: True/False/None points to add/sub/reset
	def markApply(self, _mark, _elA, part=None, step=None):
		if not self.getScene():
			return


		if part==True:
			self.getScene().markGeoAdd(_mark, _elA)

		if part==False:
			self.getScene().markGeoSub(_mark, _elA)

		if part==None:
			self.getScene().markGeoSub(_mark)
			if _elA:
				self.getScene().markGeoAdd(_mark, _elA)


		self.getScene().marksReapply(step)



	def objectApply(self, _elA, _data={}):
		if not self.getScene():
			return


		self.getScene().geoDataSet(_elA, _data)
