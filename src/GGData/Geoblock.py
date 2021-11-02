import xml.etree.ElementTree as XML
import re

from .GGen import *



# -todo 181 (decide) +0: geometry embed method
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


	xformOffset = (0,0)
	xformScale = (1,1)
	geoXML = None
	allItems = []
	source = ''
	name = ''


	dirtyFlag = False



	def __init__(self, _source, _name=''):
		self.name = _name

		self.source = _source
		self.geoXML = XML.parse(_source)
		self.allItems = []


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
				self.allItems.append( Geoitem(cTag, cName) )

				i += 1


	def xformSet(self, offset=None, scale=None):
		if offset:
			self.xformOffset = offset

			self.dirtyFlag = True

		if scale:
			self.xformScale = scale

			self.dirtyFlag = True


		return [(self.xformScale[0],0), (0,self.xformScale[1]), self.xformOffset]



	def label(self):
		return self.name



	def isDirty(self):
		for cObj in self.allItems:
			if cObj.isDirty():
				return True


		return self.dirtyFlag



	def clean(self):
		for cObj in self.allItems:
			cObj.clean()


		self.dirtyFlag = False



	def xmlRoot(self, _string):
		cRoot = self.geoXML.getroot()
		return (XML.tostring(cRoot) if _string else cRoot)



	def getGeo(self, _nameA=True):
		return [cI for cI in self.allItems if (_nameA==True or (cI.name in _nameA))]



	def packGeo(self, _markLimit):
		out = {
			'xform': self.xformSet(),
			'source': self.source,
			'name': self.name
		}


		geoA = []

		for cObj in self.allItems:
			geoA.append( cObj.packItem(_markLimit) )

		out['items'] = geoA

		return out



# -todo 104 (module-data, decide) +0: move to filter
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def trace(self, _x=0, _y=0):
		cScene = self.xmlRoot(False)


		cGG = GGen(cScene)
		cGG.set(
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
		)

		def shapePreHook(_element):
			refGeo = self.getGeo([_element.get('id')])

			if not refGeo:
				return False

			if not refGeo[0].dataGet('visible', True):
				return False


			return 'G0'


		def shapeInHook(_element, _point):
			refGeo = self.getGeo([_element.get('id')])
			cycle = refGeo[0].dataGet('Laser Cycle', 100)
			return( f"S{int(cycle)} G1" )

		cGG.set(shapeIn=shapeInHook, shapePre=shapePreHook)



		xf = self.xformOffset

		gFlat = []
		for g in cGG.generate( xform=[[1,0,xf[0]+_x], [0,-1,-xf[1]+_y]] ):
			gFlat += g


		return gFlat



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



	def packItem(self, _markLimit=[]):
		out = {
			'name': self.name,
			'data': self.dataOwn
		}


		out['marks'] = [_markLimit.index(cMark) for cMark in self.marks if (cMark in _markLimit)]


		return out



	def setTag(self, _tag, _data, dirty=True):
		self.obj.set(_tag, _data)


		if dirty:
			self.dirtyGeo = True



	#Non-Scene Marks should not make dirty
	def markSet(self, _mark, _on, dirty=True):
		if _on:
			if _mark in self.marks:
				return

			self.marks.append(_mark)

		else:
			if _mark not in self.marks:
				return

			self.marks.remove(_mark)


		self.dirtyRuntime = True
		if dirty:
			self.dirtyBind = True


		return True



	def markAssigned(self, _mark):
		return _mark in self.marks



	def markList(self):
		return list(self.marks)



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
