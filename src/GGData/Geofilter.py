'''
Object proccessing functions.
Applied to provided geometry with provided data.
'''

class Geofilter():
	name = ''	# Reference name for creation by GGData.markNew()
	step = ''	# Step of executution (TO BE FILLED)
	dataOwn = {}	# Internal data provided at init
	dataPublic = {}	# Data to be returned on Geolayer.marksSolve() cycle, respecting step



# Init filter with provided data dict to be private
	def __init__(self, _data={}):
		self.dataOwn = _data
		self.dataPublic = {}



# Return public output data, which is blank if not filled by overloaded .run()
	def proccess(self, _step, _geo, _data):
		if _step != self.step:
			return

		return self.run(_geo, _data)



	def getData(self, _step):
		if _step != self.step:
			return {}

		return dict(self.dataPublic)


### OVERLOAD ###


# Main proccess function for overload in derived filters.
# Called from Geomark.
#
# Return True if provided geometry is modified inline
	def run(self, _geo, _data):
		return False
