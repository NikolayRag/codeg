'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	allFilters = []


	name = ''
	step = ''
	data = None



	def list(system=False):
		return [f for f in Geofilter.allFilters]



	def __init__(self, _data):
		self.data = _data


		Geofilter.allFilters.append(self)



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
