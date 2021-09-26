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
	markData = {}
	markFilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.markData = _data
		self.markFilter = _filter

		self.priority = _priority



	def applyFilter(self, _geo, _step):
		outData = dict(self.markData)


		if _step and self.markFilter and (self.markFilter.step == _step):
			filterData = self.markFilter.proccess(_geo, self.markData)

			for cData in filterData:
				outData[cData] = filterData[cData]


		return outData
