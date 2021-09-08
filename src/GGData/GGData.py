# =todo 90 (ux, module-ui, fix) +0: respect units - both svg and device

# =todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

#  todo 105 (module-data, filter, API) +0: add geo Filter class

import xml.etree.ElementTree as XML
import re


from GGen import *
from .Scene import *
from .Decorator import *



class GGData():
	CachedFields = {
		'vector-effect': 'svg-vector-effect',
		'stroke': 'svg-stroke',
		'stroke-width': 'svg-stroke-width',
		'stroke-dasharray': 'svg-stroke-dasharray',
		'fill': 'svg-fill',
		'opacity': 'svg-opacity',
		'display': 'svg-display'
	}


	theGG = None
	namedRef = {}

	scene = None
	staticDecor = []


	def __init__(self):
		self.staticDecor = []



#  todo 84 (module-data) +0: make file load (save) plugin system
	def newScene(self, _fileName):
		self.scene = Scene(self.staticDecor)


		self.theGG = XML.parse(_fileName)
		self.namedRef = {}


		i = 1
		for cTag in self.theGG.iter():
			tagType = cTag.tag[28:]

			if tagType == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if tagType == 'g':
				None

			if tagType in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in self.CachedFields:
					cTag.set(self.CachedFields[cField], cTag.get(cField) or '')


				self.namedRef[tagType +str(i)] = cTag

				i += 1


		return {cN:{'on':True} for cN in self.namedRef}



	def getXML(self):
		if not self.theGG:
			return False

		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



#  todo 104 (module-dispatch, decide) +0: move to dispatch
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.theGG:
			return

#  todo 100 (gcode, feature) +0: allow flexible filters for gcode
		cGG = GGen(self.theGG.getroot())
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



# -todo 111 (decorator, optimize) +0: dramatically slow
	def setTags(self, _name, _tags):
		cEl = self.namedRef[_name]
		for cTag in _tags:
			cEl.set(cTag, _tags[cTag])




	def decorNew(self, _tags, _priority=0, persistent=False):
		cDec = Decorator(_tags, _priority)
		if persistent:
			self.staticDecor.append(cDec)

		if self.scene:
			self.scene.decoratorAdd(cDec)

		return cDec



	def decorSet(self, _dec, _elA, add=None):
		if add==None:
			_dec.assign(_elA)

		elif add:
			_dec.add(_elA)

		else:
			_dec.sub(_elA)


		if not self.scene:
			return


		toDecorate = self.scene.decoratorsOrder(self.namedRef.keys())
		for cName in toDecorate:
			for cDec in toDecorate[cName]:
				self.setTags(cName, cDec.tags)

