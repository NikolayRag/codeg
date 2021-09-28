'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	name = ''
	step = ''
	dataOwn = {}
	dataPublic = {}



	def __init__(self, _data={}):
		self.dataOwn = _data
		self.dataPublic = {}



	# return False, new geo, or True if provided geo is modified
	def proccess(self, _geo, _data):
		return False



	def dataGet(self):
		return dict(self.dataPublic)
