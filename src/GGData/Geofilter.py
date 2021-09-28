'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	name = ''
	step = ''
	dataOwn = {}
	dataPublic = {}



# Init filter with provided data dict to be private
	def __init__(self, _data={}):
		self.dataOwn = _data
		self.dataPublic = {}



	def isStep(self, _step):
		return _step == self.step



# Main proccess function for overload in derived filters.
# Called from Geomark.
#
# Return:
# False = geometry unmodified
# True = geometry modified
# (reserved) newGeo = totally new geometry
	def proccess(self, _geo, _data):
		return False



# Return public output data, which is blank if not filled by .proccess()
	def dataGet(self):
		return dict(self.dataPublic)
