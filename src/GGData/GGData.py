# -todo 9 (spec, module-data) +1: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
# -todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

import xml.etree.ElementTree as XML
import re


from GGen import *



class GGData():
	CachedFields = {
		'stroke': 'originalStroke',
		'stroke-width': 'originalStrokeWidth',
		'stroke-dasharray': 'originalStrokeDash',
		'fill': 'originalFill',
		'opacity': 'originalOpacity',
		'display': 'originalDisplay'
	}


	theGG = None
	namedRef = {}


#  todo 84 (module-data) +0: make file load (save) plugin system
	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)
		self.namedRef = {}


		meta = {}

		i = 1
		for a in self.theGG.iter():
			aTag = a.tag[28:]

			if aTag == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if aTag == 'g':
				None

			if aTag in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in self.CachedFields:
					a.set(self.CachedFields[cField], a.get(cField) or '')


				self.namedRef[aTag +str(i)] = a
				meta[aTag +str(i)] = {'on':True}

				i += 1


		return {'meta': meta, 'xml':self.getXML()}



	def getXML(self):
		if not self.theGG:
			return False

		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



# -todo 66 (module-ui) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.theGG:
			return

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



	def override(self, _name, _style={}):
		if not _name:
			return

		cEl = self.namedRef[_name]

		for cField in _style:
			newVal = _style[cField] or cEl.get(self.CachedFields[cField])
			cEl.set(cField, newVal)
