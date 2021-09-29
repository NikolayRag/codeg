'''
Object proccessing functions.
Applied to provided geometry with provided data.
Used internally, have no public access.

Base class for deriving filters.
Derived class should override .run() function, and fill out dataPublic.
'''

class Geofilter():
	step = ''	# Step of executution (TO BE FILLED)
	dataOwn = {}	# Internal data provided at init
	dataPublic = {}	# Data to be returned on Geolayer.marksSolve() cycle, at particular step



# Init filter with provided data dict to be private
	def __init__(self, _data={}):
		self.dataOwn = dict(_data)
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



	def setData(self, _data, clean=False):
		if clean:
			self.data = dict(_data)

			return


		for n in _data:
			self.data[n] = _data[n]



### OVERLOAD ###


# Main proccess function for overload in derived filters.
# Called from Geomark.
#
# Return True if provided geometry is modified inline or dataPublic is updated
	def run(self, _geo, _data):
		return False
