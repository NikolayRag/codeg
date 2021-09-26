'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	name = ''
	step = ''
	data = None



	def __init__(self, _data):
		self.data = _data



	# return False, new geo, or True if provided geo is modified
	# Data used is own-defined format
	def proccess(self, _geo, _data):
		return False




class FilterSetSVG(Geofilter):
	name = 'setSVG'
	step = 'UI'



	def proccess(self, _geo, _data):
		for cTag in self.data:
			_geo.setTag(cTag, self.data[cTag])


		return self.data
