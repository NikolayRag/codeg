# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

# =todo 11 (spec, module-data) +0: read/save scene format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

#  todo 105 (module-data, filter, API) +0: add geo Filter class

'''
Data scope:
	(Filter,)
	(Scene,)
		(Mark,)
			*Filter link
		(Geoblock,)/(Geo,)
			*Mark link

'''


from GGen import *
from .Scene import *
from .Geofilter import *
from .Geomark import *



class GGData():

	allFilters = {}

	allScenes = []
	sceneActive = -1



	def __init__(self):
		self.allFilters = {a.name:a for a in Geofilter.__subclasses__()}



	def newScene(self):
		self.allScenes.clear()

		self.allScenes.append( Scene() )
		self.sceneActive = len(self.allScenes) -1

		for cMark in Geomark.allMarks___:
			cMark.resetAssigned(True)


	def getScene(self):
		return self.sceneActive>=0 and self.allScenes[self.sceneActive]




# -todo 84 (module-data) +0: make file load (save) plugin system
	def loadGeo(self, _source, _type='svg'):
		self.getScene().geoAdd(_source, _type)

		return self.getScene().geoMeta()



	def getXML(self):
		return (self.getScene() and self.getScene().getSceneXML(True))



	def available(self):
		return bool(self.getScene())



# -todo 104 (module-dispatch, decide) +0: move to dispatch
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

		def shapeInHook(_element, _point):
			return( "S100 G1" )
		cGG.set(shapeIn = shapeInHook)


		gFlat = []
		for g in cGG.generate( xform=[[1,0,x], [0,-1,y]] ):
			gFlat += g

		return "\n".join(gFlat)



	def markNew(self, data=None, filterName=None, filterData=None, priority=0, scene=False):
		filterProc = (filterName in self.allFilters) and self.allFilters[filterName](filterData)

		cMark = Geomark(data, priority, filterProc)
		if scene and self.getScene():
			self.getScene().markAdd(cMark)

		return cMark



	# add: True/False to add/sub, other to reset
	def markApply(self, _mark, _elA, add=None, step=None):
		if add==True:
			_elA = set(_mark.assignedList___ + _elA)

		if add==False:
			_elA = set(_mark.assignedList___).difference(_elA)


		_mark.assignGeo(_elA)


		self.getScene() and self.getScene().marksReapply(step)
