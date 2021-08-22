#  todo 9 (spec, module-data) +0: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
# -todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

import xml.etree.ElementTree as XML
import re


from GGen import *



class GGData():
	theGG = None
	namedRef = {}


#  todo 84 (module-data) +0: make file load (save) plugin system
	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)
		self.namedRef = {}


		i = 1
		for a in self.theGG.iter():
			aTag = a.tag[28:]

			if aTag == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if aTag == 'g':
				None

			if aTag in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				a.set('originalStroke', a.get('stroke') or '')
				a.set('originalStrokeWidth', a.get('stroke-width') or '')
				a.set('originalStrokeDash', a.get('stroke-dasharray') or '')
				a.set('originalFill', a.get('fill') or '')
				a.set('originalOpacity', a.get('opacity') or '')
				a.set('originalDisplay', a.get('display') or '')

				self.namedRef[aTag +str(i)] = a

				i += 1


		return {'meta': self.namedRef.keys(), 'xml':self.getXML()}



	def getXML(self):
		if not self.theGG:
			return False

		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



# =todo 22 (module-dispatch, ux) +0: make dispatch interruptable
# =todo 85 (module-dispatch) +0: Gcode generate in background
# -todo 66 (module-ui) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.theGG:
			return

# =todo 76 (fix, gcode) +0: gcode move, scale and crop
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
		for g in cGG.generate( xform=[[1,0,0], [0,-1,y]] ):
			gFlat += g

		return "\n".join(gFlat)



	def override(self, _name, _style={}):
		if not _name:
			return

		cEl = self.namedRef[_name]

		cEl.set('display', _style['display'] if 'display' in _style else cEl.get('originalDisplay'))
		cEl.set('opacity', _style['opacity'] if 'opacity' in _style else cEl.get('originalOpacity'))
		cEl.set('fill', _style['fill'] if 'fill' in _style else cEl.get('originalFill'))
		cEl.set('stroke', _style['stroke'] if 'stroke' in _style else cEl.get('originalStroke'))
		cEl.set('stroke-width', _style['stroke-width'] if 'stroke-width' in _style else cEl.get('originalStrokeWidth'))
		cEl.set('stroke-dasharray', _style['stroke-dasharray'] if 'stroke-dasharray' in _style else cEl.get('originalStrokeDash'))
