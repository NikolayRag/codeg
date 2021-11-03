from xml.etree import ElementTree
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
	svgeo = None
	allItems = []
	source = ''
	name = ''


	dirtyFlag = False



	def __init__(self, _source, _name=''):
		self.name = _name

		self.source = _source
		geoXML = ElementTree.parse(_source)
		self.svgeo = GGen(geoXML.getroot())

		self.allItems = []


		i = 1
		for cEl in self.svgeo.tree():
			cName = cEl.type() +str(i)
			cItem = Geoitem(cEl, cName)
			cEl.setData(cItem)

			self.allItems.append(cItem)
			i += 1


	def xformSet(self, offset=None, scale=None):
		if offset:
			self.xformOffset = offset

			self.dirtyFlag = True

		if scale:
			self.xformScale = scale

			self.dirtyFlag = True


		return [(self.xformScale[0],0,self.xformOffset[0]), (0,self.xformScale[1],self.xformOffset[1])]



	def boxed(self, _xmm, _ymm, strict=True):
		out = []
		_xmm = (_xmm[0]-self.xformOffset[0], _xmm[1]-self.xformOffset[0])
		_ymm = (_ymm[0]-self.xformOffset[1], _ymm[1]-self.xformOffset[1])

		for cObj in self.allItems:
			cBox = cObj.bbox()
			if strict:
				if (_xmm[0]<cBox[0]) and (_xmm[1]>cBox[1]) and (_ymm[0]<cBox[2]) and (_ymm[1]>cBox[3]):
					out.append(cObj)
			else:
				if not( (_xmm[1]<cBox[0]) or (_xmm[0]>cBox[1]) or (_ymm[1]<cBox[2]) or (_ymm[0]>cBox[3]) ):
					out.append(cObj)

		return out



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



	def xmlString(self):
		return ElementTree.tostring(self.svgeo.root())



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
		def shapePreHook(_shape):
			refItem = _shape.data()
			if not refItem.dataGet('visible', True):
				return False

			return 'G0'


		def shapeInHook(_shape, _point):
			refItem = _shape.data()
			cycle = refItem.dataGet('Laser Cycle', 100)

			return( f"S{int(cycle)} G1" )


		self.svgeo.set(shapeIn=shapeInHook, shapePre=shapePreHook, shapeOut = 'S0')

		xf = self.xformOffset
		out = []
		for g in self.svgeo.generate( xform=[[1,0,xf[0]+_x], [0,-1,-xf[1]+_y]] ):
			out += g


		return out



class Geoitem():
	ggobj = None
	box = None
	name = ''

	marks = []

	dataOwn = {}
	dataApplied = {}

	dirtyGeo = False
	dirtyData = False
	dirtyBind = False
	dirtyRuntime = False


	def __init__(self, _ggobj, _name='', _data={}):
		self.ggobj = _ggobj
		self.box = self.ggobj.bBox(True)
		self.name = _name

		self.marks = []

		self.dataOwn = dict(_data)
		self.dataApplied = dict(self.dataOwn)

		self.dirtyGeo = False
		self.dirtyData = False
		self.dirtyBind = False
		self.dirtyRuntime = False



	def bbox(self): 
		return self.box



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
		self.ggobj.xml().set(_tag, _data)


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
