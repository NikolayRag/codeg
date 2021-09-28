'''
Geometry marker.
Hold arbitrary data and optional Geofilter to be applied
 to objects attached at particular steps of runtime/
'''


class Geomark():
	data = {}
	gfilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.data = dict(_data)
		self.gfilter = _filter

		self.priority = _priority



# -todo 136 (module-data, decide) +0: step is ambiguous
	def applyFilter(self, _geo, _step):
		outData = dict(self.data)


		if self.gfilter:
			self.gfilter.proccess(_step, _geo, self.data)

			filterData = self.gfilter.getData(_step)

			for cData in filterData:
				outData[cData] = filterData[cData]


		return outData


### ###


	def setPriority(self, _priority):
		self.priority = _priority



	def getPriority(self):
		return self.priority



	def setData(self, _data, clean=False):
		if clean:
			self.data = dict(_data)

			return


		for n in _data:
			self.data[n] = _data[n]



	def getData(self):
		return dict(self.data)
