'''
'''


class Geomark():
	data = {}
	gfilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.data = dict(_data)
		self.gfilter = _filter

		self.priority = _priority



	def applyFilter(self, _geo, _step):
		outData = dict(self.data)


		if self.gfilter:
			self.gfilter.proccess(_step, _geo, self.data)

			filterData = self.gfilter.getData(_step)

			for cData in filterData:
				outData[cData] = filterData[cData]


		return outData
