#  todo 9 (spec, module-data) +0: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
# -todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

import xml.etree.ElementTree as XML


from svg_to_gcode import svg_parser
from svg_to_gcode.compiler import Compiler, interfaces



class GGData():
	theGG = None



	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)

		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



	def getG(self):
		if not self.theGG:
			return


		gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=100, pass_depth=1)

		ggCurves = svg_parser.parse_root(self.theGG.getroot(), True, 100)
		gcode_compiler.append_curves(ggCurves)

		cGcode = gcode_compiler.compile()


		return cGcode

