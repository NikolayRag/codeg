'''
Applied to Geoblock by Geomark, 
'''

class Geofilter():
	allFilters = []



	def list(system=False):
		return [f for f in Geofilter.allFilters if f.isSystem==system]



	def __init__(self):
		self.isSystem = True

		Geofilter.allFilters.append(self)



	# return False, new geo, or True if provided geo is modified
	def proccess(self, _geo, _data):
		return False





class FilterSetSVG(Geofilter):

	def proccess(self, _geo, _data):
		for cTag in _data:
			_geo.set(cTag, _data[cTag])


		return True