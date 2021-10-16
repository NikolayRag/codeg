import xml.etree.ElementTree as XML
import re


class Geoblock():
	# Should contain fields affected by Marks
	CachedFields = [
		'id',
		'vector-effect',
		'stroke',
		'stroke-width',
		'stroke-dasharray',
		'fill',
		'opacity',
		'display'
	]


	geoXML = None
	namedLayers = {}
	namespace = ''


	dirtyFlag = False



	def __init__(self, _source, _type):
		self.namespace = _source
		self.geoXML = XML.parse(_source)
		self.namedLayers = {}


		i = 1
		for cTag in self.geoXML.iter():
			tagType = cTag.tag[28:]

			if tagType == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if tagType == 'g':
				None

			if tagType in ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in Geoblock.CachedFields:
					cTag.set('cache-'+cField, cTag.get(cField) or '')

				cName = tagType +str(i)
				cTag.set('id', cName)
				self.namedLayers[cName] = Geoitem(cTag, cName)

				i += 1



	def isDirty(self):
		for cObj in self.namedLayers:
			if self.namedLayers[cObj].isDirty():
				return True


		return self.dirtyFlag



	def clean(self):
		for cObj in self.namedLayers:
			self.namedLayers[cObj].clean()


		self.dirtyFlag = False



	def xmlRoot(self, _string):
		cRoot = self.geoXML.getroot()
		return (XML.tostring(cRoot) if _string else cRoot)



	def getObj(self, _nameA=True):
		if _nameA == True:
			_nameA = self.names()

		return [self.namedLayers[n] for n in _nameA if (n in self.namedLayers)]



	def names(self):
		return self.namedLayers.keys()


	def dataSet(self, _el, _data):
		if not _el in self.namedLayers:
			return

		self.namedLayers[_el].dataSet(_data)



class Geoitem():
	obj = None
	name = ''

	marks = []

	dataOwn = {}
	dataApplied = {}

	dirtyGeo = False
	dirtyData = False
	dirtyBind = False
	dirtyRuntime = False


	def __init__(self, _obj, _name='', _data={}):
		self.obj = _obj
		self.name = _name

		self.marks = []

		self.dataOwn = dict(_data)
		self.dataApplied = dict(self.dataOwn)

		self.dirtyGeo = False
		self.dirtyData = False
		self.dirtyBind = False
		self.dirtyRuntime = False



	def isDirty(self): 
		return (self.dirtyGeo or self.dirtyData or self.dirtyBind)



	def clean(self):
		self.dirtyGeo = False
		self.dirtyData = False 
		self.dirtyBind = False



	def setTag(self, _tag, _data, dirty=True):
		self.obj.set(_tag, _data)


		if dirty:
			self.dirtyGeo = True



	def markAdd(self, _mark, dirty=True):
		if _mark in self.marks:
			return


		self.marks.append(_mark)

		self.dirtyRuntime = True
		if dirty:
			self.dirtyBind = True


		return True



	def markSub(self, _mark, dirty=True):
		if _mark not in self.marks:
			return


		self.marks.remove(_mark)

		self.dirtyRuntime = True
		if dirty:
			self.dirtyBind = True


		return True



#  todo 133 (mark, optimize, decide) -1: Need to cache data?
	def marksSolve(self, filterStep=None):
		self.dataApplied = dict(self.dataOwn)

		markSortedA = sorted(self.marks, key=lambda m: m.priority)


		for cMark in markSortedA:
			filterData = cMark.applyFilter(self, self.dirtyRuntime and filterStep)

			for cData in filterData:
				self.dataApplied[cData] = filterData[cData]


		self.dirtyRuntime = False


### DATA ###


	def dataGet(self, _field=None, _default=None):
		self.marksSolve()


		if not _field:
			return dict(self.dataApplied)


		if _field in self.dataApplied:
			return self.dataApplied[_field]


		return _default



	def dataSet(self, _data):
		for dName in _data:
			self.dataOwn[dName] = _data[dName]


		self.dirtyData = True
