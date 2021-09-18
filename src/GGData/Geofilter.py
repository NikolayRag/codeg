'''
Applied to Geoblock by Geomark, 
'''

class Geofilter():
	def __init__(self):
		self.isSystem = True


	# return False, new geo, or True if provided geo is modified
	def proccess(self, _geo, _data):
		return False





class FilterSetSVG(Geofilter):

	def proccess(self, _geo, _data):
		for cTag in _data:
			_geo.set(cTag, _data[cTag])


		return True