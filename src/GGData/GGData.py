import xml.etree.ElementTree as XML


from pygcode import *



class GGData():
	theGG = None



	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)

		return XML.tostring(self.theGG.getroot())



	def saveG(self):
		gcodes = [
			GCodeRapidMove(Z=5),
			GCodeStartSpindleCW(),
			GCodeRapidMove(X=10, Y=20),
			GCodeFeedRate(200),
			GCodeLinearMove(Z=-1.5),
			GCodeRapidMove(Z=5),
			GCodeStopSpindle(),
		]
		print('\n'.join(str(g) for g in gcodes))
