'''
Geometry applied set of data
Holds filter function, filter roadpoint and supply data to be applied
to object layer

Filter roadpoint is one of several known origins:
- at creation/load
- at user explicit action
- at output
'''


class Geomark():
#  todo 129 (mark) +0: store custom fields data list
	data = {}
	gfilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.data = _data
		self.gfilter = _filter

		self.priority = _priority



	def applyFilter(self, _geo, _step):
		outData = dict(self.data)


		if self.gfilter and (self.gfilter.step == _step):
			if _step:
				self.gfilter.proccess(_geo, self.data)

			
			filterData = self.gfilter.dataGet()

			for cData in filterData:
				outData[cData] = filterData[cData]


		return outData
