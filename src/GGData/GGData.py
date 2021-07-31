import xml.etree.ElementTree as XML


from svg_to_gcode import svg_parser
from svg_to_gcode.compiler import Compiler, interfaces



class GGData():
	theGG = None



	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)

		return XML.tostring(self.theGG.getroot())



	def saveG(self, _fileName):
		if not self.theGG:
			return


		gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=100, pass_depth=1)

		ggCurves = svg_parser.parse_root(self.theGG.getroot(), True, 100)
		gcode_compiler.append_curves(ggCurves)

		cGcode = gcode_compiler.compile()


		with open(_fileName, 'w') as f:
			f.write(cGcode)

