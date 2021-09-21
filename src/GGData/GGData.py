# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

# =todo 11 (spec, module-data) +0: read/save scene format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

#  todo 105 (module-data, filter, API) +0: add geo Filter class

'''
Data scope:

Application
	(Filter,) +data
	(Scene,)
		(Mark,) +data
			*Filter link
		(Geoblock,)/(Geo,) +data
			*Mark link

'''


from GGen import *
from .Scene import *
from .Geofilter import *
from .Geomark import *
from .Geoblock import *



class GGData():
	prefilterSVGTags = 1


	scene = None


	def __init__(self):
		None



	def newScene(self):
		self.scene = Scene()

		for cMark in Geomark.allMarks:
			cMark.reset(True)




# -todo 84 (module-data) +0: make file load (save) plugin system
	def loadGeo(self, _source, _type='svg'):
		self.scene.geoAdd( Geoblock(_source, _type) )

		return self.scene.geoMeta()



	def getXML(self):
		return (self.scene and self.scene.getSceneXML(True))



	def available(self):
		return bool(self.scene)



# -todo 104 (module-dispatch, decide) +0: move to dispatch
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.scene:
			return

#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cGG = GGen(self.scene.getSceneXML())
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



	def markNew(self, data=None, filterData=None, priority=0, filterAt=None):
		filterProc = None

		if filterAt=='UI':
			filterProc = FilterSetSVG(filterData)

		return Geomark(data, priority, filterProc, filterAt)





	# add: True/False to add/sub, other to reset
	def markApply(self, _mark, _elA, add=None, at=None):
		if add==True:
			_elA = set(_mark.assignedList + _elA)

		if add==False:
			_elA = set(_mark.assignedList).difference(_elA)


		_mark.assignGeo(_elA)


		self.scene and self.scene.marksReapply(at)
