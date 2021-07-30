import xml.etree.ElementTree as XML


class GGData():
	theGG = None



	def cbUIFileLoad(self, _fileName):
		self.theGG = XML.parse(_fileName)

		return XML.tostring(self.theGG.getroot())
