#  todo 9 (spec, module-data) +0: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
# -todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

import xml.etree.ElementTree as XML
import re


from svg_to_gcode import svg_parser
from svg_to_gcode.compiler import Compiler, interfaces



class GGData():
	theGG = None
	namedRef = {}


	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)
		self.namedRef = {}


		i = 1
		for a in self.theGG.iter():
			aTag = a.tag[28:]

			if aTag == 'xml':
				None

			if aTag == 'g':
				None

			if aTag in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				a.set('originalFill', a.get('fill') or '')
				a.set('originalOpacity', a.get('opacity') or '')
				a.set('originalDisplay', a.get('display') or '')
				self.namedRef[aTag +str(i)] = a
				i += 1


		return {'meta': self.namedRef.keys(), 'xml':self.getXML()}



	def getXML(self):
		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



	def getG(self):
		if not self.theGG:
			return


		gcode_compiler = Compiler(interfaces.Gcode, movement_speed=10000, cutting_speed=10000, pass_depth=1)

		ggCurves = svg_parser.parse_root(self.theGG.getroot(), True, 100)
		gcode_compiler.append_curves(ggCurves)

		cGcode = gcode_compiler.compile()


		return cGcode



	def override(self, _name, _style={}):
		if not _name:
			return

		cEl = self.namedRef[_name]

		cEl.set('display', _style['display'] if 'display' in _style else cEl.get('originalDisplay'))
		cEl.set('opacity', _style['opacity'] if 'opacity' in _style else cEl.get('originalOpacity'))
		cEl.set('fill', _style['fill'] if 'fill' in _style else cEl.get('originalFill'))

