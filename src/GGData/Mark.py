'''
Geometry marker.
Hold arbitrary data and optional Markfilter to be applied
 to objects attached at particular steps of runtime.
'''


class Mark():
	isDirty = False
	data = {}
	gfilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.isDirty = False

		self.data = dict(_data)
		self.gfilter = _filter

		self.priority = _priority



# -todo 136 (module-data, decide) +0: step is ambiguous
	def applyFilter(self, _geo, _step):
		outData = dict(self.data)


		if self.gfilter:
			if self.gfilter.proccess(_step, _geo, self.data):
				self.isDirty = True

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



	def getData(self, _field=None, _default=None):
		if _field==None:
			return dict(self.data)


		if _field in self.data:
			return self.data[_field]

		return _default