from xml.etree import ElementTree
import re

from .GGen import *


#  todo 236 (svg, fix, v2) +0: parse svg more completely

# -todo 181 (decide) +0: geometry embed method
class Geoblock():
	matrix = [[1,0,0],[0,1,0]]
	svgeo = None
	allItems = []
	box = None
	source = ''
	name = ''


	dirtyFlag = False



	def __init__(self, _source, _name='', raw=False):
		self.matrix = [[1,0,0],[0,1,0]]

		self.name = _name
		self.source = _source

		if raw:
			geoXML = ElementTree.fromstring(self.source)
		else:
			geoXML = ElementTree.parse(self.source).getroot()
		self.svgeo = GGen(geoXML)

		self.allItems = []


		i = 1
		for cEl in self.svgeo.tree():
			cName = cEl.type() +str(i)
			cItem = Geoitem(cEl, cName)
			cEl.setData(cItem)

			self.allItems.append(cItem)
			i += 1


	def xformSet(self, _matrix=None, offset=None, scale=None):
		if _matrix:
			self.matrix = _matrix

		if offset:
			self.matrix[0][2] = offset[0]
			self.matrix[1][2] = offset[1]

			self.dirtyFlag = True

		if scale:
			self.matrix[0][0] = scale[0]
			self.matrix[1][1] = scale[1]

			self.dirtyFlag = True


		return self.matrix



	def bbox(self):
		bbox = None if self.allItems else [0,0,0,0]

		for cObj in self.allItems:
			cBox = list(cObj.bbox())
			bbox = bbox or cBox

			if bbox[0]>cBox[0]: bbox[0]=cBox[0]
			if bbox[1]<cBox[1]: bbox[1]=cBox[1]
			if bbox[2]>cBox[2]: bbox[2]=cBox[2]
			if bbox[3]<cBox[3]: bbox[3]=cBox[3]


		bbox = [
			bbox[0]*self.matrix[0][0]+self.matrix[0][2],
			bbox[1]*self.matrix[0][0]+self.matrix[0][2],
			bbox[2]*self.matrix[1][1]+self.matrix[1][2],
			bbox[3]*self.matrix[1][1]+self.matrix[1][2],
		]

		return bbox


	def boxed(self, _xmm, _ymm, strict=True):
		out = []
		_xmm = ((_xmm[0]-self.matrix[0][2])/self.matrix[0][0], (_xmm[1]-self.matrix[0][2])/self.matrix[0][0])
		_ymm = ((_ymm[0]-self.matrix[1][2])/self.matrix[1][1], (_ymm[1]-self.matrix[1][2])/self.matrix[1][1])

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
			'xform': self.matrix,
			'source': self.source,
			'name': self.name
		}


		geoA = []

		for cObj in self.allItems:
			geoA.append( cObj.packItem(_markLimit) )

		out['items'] = geoA

		return out



# -todo 104 (module-data, unsure) +0: move to filter
	def trace(self, _x=0, _y=0, shapePre='', shapeIn='', shapeOut='', passes=1):
		self.svgeo.set(shapePre=shapePre, shapeIn=shapeIn, shapeOut=shapeOut)

		xform=[
			[self.matrix[0][0], 0, self.matrix[0][2]+_x],
			[0, self.matrix[1][1]*-1, -self.matrix[1][2]+_y]
		]

		out = []
		for sh, gA in self.svgeo.generate( xform=xform ):
			cPasses = passes
			if callable(cPasses) and sh:
				cPasses = cPasses(sh)

			for i in range(cPasses):
				out += gA


		return out



class Geoitem():
	ggobj = None
	box = None
	name = ''

	marks = []

	dataOwn = {}

	dirtyGeo = False
	dirtyData = False
	dirtyBind = False
	dirtySolve = False


	def __init__(self, _ggobj, _name='', _data={}):
		self.ggobj = _ggobj
		self.name = _name

		self.dataOwn = dict(_data)

		self.marks = []

		self.dirtyGeo = False
		self.dirtyData = False
		self.dirtyBind = False
		self.dirtySolve = False



#  todo 233 (performance, unsure) +0: bBox maybe time consuming for complex geo
	def bbox(self): 
		if not self.box:
			self.box = self.ggobj.bBox(True)

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



	#Non-Scene Marks should not set dirty
	def markSet(self, _mark, _on, dirty=True):
		if _on:
			if _mark in self.marks:
				return

			self.marks.append(_mark)

		else:
			if _mark not in self.marks:
				return

			self.marks.remove(_mark)


		self.dirtySolve = True
		if dirty:
			self.dirtyBind = True


		return True



	def markAssigned(self, _mark):
		return _mark in self.marks



	def markList(self):
		return list(self.marks)



#  todo 133 (mark, optimize, unsure) -1: Need to cache data?
	def marksSolve(self, filterStep=None, force=False):
		dataApplied = dict(self.dataOwn)

		markSortedA = sorted(self.marks, key=lambda m: m.priority)


		for cMark in markSortedA:
			filterData = cMark.applyFilter(self, (self.dirtySolve or force) and filterStep)

			for cData in filterData:
				dataApplied[cData] = filterData[cData]


		self.dirtySolve = False

		return dataApplied



### DATA ###


	def dataGet(self, _field=None, _default=None):
		markData = self.marksSolve()


		if not _field:
			return markData


		if _field in markData:
			return markData[_field]


		return _default



	def dataSet(self, _data):
		for dName in _data:
			self.dataOwn[dName] = _data[dName]


		self.dirtyData = True
