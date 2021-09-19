'''
Object proccessing functions.
Applied to provided goemetry with provided data
'''

class Geofilter():
	allFilters = []


	ownData = None



	def list(system=False):
		return [f for f in Geofilter.allFilters if f.isSystem==system]



	def __init__(self, _data):
		self.isSystem = True

		self.ownData = _data


		Geofilter.allFilters.append(self)



	# return False, new geo, or True if provided geo is modified
	def proccess(self, _geo, _data):
		return False





class FilterSetSVG(Geofilter):

	def proccess(self, _geo, _data):
		for cTag in self.ownData:
			_geo.set(cTag, self.ownData[cTag])


		return True