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



	def proccess(self, _step, _geo, _data):
		if _step != self.step:
			return

		return self.run(_geo, _data)



	def getData(self, _step):
		if _step != self.step:
			return {}

		return dict(self.dataPublic)



# Main proccess function for overload in derived filters.
# Called from Geomark.
#
# Return True if provided geometry is modified inline
	def run(self, _geo, _data):
		return False
