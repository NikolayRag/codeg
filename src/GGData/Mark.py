'''
Geometry marker.
Hold arbitrary data and optional Markfilter to be applied
 to objects attached at particular steps of runtime.
'''


class Mark():
	dirtyFlag = False
	data = {}
	gfilter = None
	priority = 0
	name = ''


	def __init__(self, _data, _priority=0, _filter=None, _name=''):
		self.dirtyFlag = False

		self.data = dict(_data)
		self.gfilter = _filter

		self.priority = _priority

		self.name = _name



	def label(self, _newName=None):
		if _newName:
			self.name = _newName

		return self.name



	def isDirty(self):
		return self.dirtyFlag



	def clean(self):
		self.dirtyFlag = False



	def packMark(self, _fields=[]):
		cData = dict(self.data)
		if _fields:
			cData = {n:v for n,v in self.data.items() if n in _fields}

		out = {
			'priority': self.priority,
			'filter': self.gfilter and self.gfilter.__name__,
			'data': cData
		}


		return out



# -todo 136 (module-data, decide) +0: step is ambiguous
	def applyFilter(self, _geo, _step):
		outData = dict(self.data)


		if self.gfilter:
#  todo 162 (module-data, mark) +0: Filter Success case
			if self.gfilter.proccess(_step, _geo, self.data):
				None

			filterData = self.gfilter.getData(_step)

			for cData in filterData:
				outData[cData] = filterData[cData]


		return outData


### ###


	def setPriority(self, _priority):
		self.dirtyFlag = True

		self.priority = _priority



	def getPriority(self):
		return self.priority



	def setData(self, _data, clean=False):
		self.dirtyFlag = True


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
