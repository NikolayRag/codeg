'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	name = ''
	step = ''
	data = {}



	def __init__(self, _data={}):
		self.data = _data



	# return False, new geo, or True if provided geo is modified
	# Data used is own-defined format
	def proccess(self, _geo, _data):
		return False



	def dataGet(self):
		return dict(self.data)




class FilterSetSVG(Geofilter):
	name = 'setSVG'
	step = 'UI'



	def proccess(self, _geo, _data):
		for cTag in self.data:
			_geo.setTag(cTag, self.data[cTag])


		return True
