# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

# =todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

#  todo 105 (module-data, filter, API) +0: add geo Filter class

from GGen import *
from .Scene import *
from .Geomark import *
from .Geoblock import *


# =todo 112 (mark, feature) +0: complex mark

class GGData():
	scene = None
	staticMarks = []


	def __init__(self):
		self.staticMarks = []



	def newScene(self):
		self.scene = Scene(self.staticMarks)



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



	def markNew(self, _tags, _priority=0, persistent=False):
		cDec = Geomark(_tags, _priority)

		if persistent:
			self.staticMarks.append(cDec)

		if self.scene:
			self.scene.markAdd(cDec)

		return cDec



	def markApply(self, _dec, _elA, add=None):
		if add==None:
			_dec.assign(_elA)

		elif add:
			_dec.add(_elA)

		else:
			_dec.sub(_elA)


		self.scene and self.scene.markReapply()
