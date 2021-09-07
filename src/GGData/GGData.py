# -todo 9 (spec, module-data) +1: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
# -todo 11 (spec, module-data) +0: read/save own format

#  todo 18 (spec, module-dispatch) +0: standalone dispatcher codegg
#  todo 19 (spec, module-dispatch) +0: send to codegg

#  todo 25 (module-data, formats) +0: load .nc gcode

import xml.etree.ElementTree as XML
import re


from GGen import *



class GGData():
	CachedFields = {
		'vector-effect': 'svg-vector-effect',
		'stroke': 'svg-stroke',
		'stroke-width': 'svg-stroke-width',
		'stroke-dasharray': 'svg-stroke-dasharray',
		'fill': 'svg-fill',
		'opacity': 'svg-opacity',
		'display': 'svg-display'
	}


	theGG = None
	namedRef = {}


#  todo 84 (module-data) +0: make file load (save) plugin system
	def loadXML(self, _fileName):
		self.theGG = XML.parse(_fileName)
		self.namedRef = {}


		i = 1
		for cTag in self.theGG.iter():
			tagType = cTag.tag[28:]

			if tagType == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if tagType == 'g':
				None

			if tagType in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in self.CachedFields:
					cTag.set(self.CachedFields[cField], cTag.get(cField) or '')


				self.namedRef[tagType +str(i)] = cTag

				i += 1


		for cDec in Decorator.decorators:
			cDec.reset()


		return {cN:{'on':True} for cN in self.namedRef}



	def getXML(self):
		if not self.theGG:
			return False

		return XML.tostring(self.theGG.getroot())



	def info(self):
		if not self.theGG:
			return False

		return True



# =todo 104 (module-dispatch) +0: move to dispatch
#  todo 66 (module-ui, module-dispatch) +0: show dispatch progress
	def getG(self, x=0, y=0):
		if not self.theGG:
			return

#  todo 100 (gcode, feature) +0: allow flexible filters
		cGG = GGen(self.theGG.getroot())
		cGG.set(
			preamble = 'G90 M4 S0',
			shapePre = 'G0',
			shapeIn = 'S100 G1',
			shapeOut = 'S0',
			postamble = 'M5 G0 X0Y0'
		)

		def shapeInHook(_element, _point):
		    return( "S100 G1" )
		cGG.set(shapeIn = shapeInHook)


		gFlat = []
		for g in cGG.generate( xform=[[1,0,x], [0,-1,y]] ):
			gFlat += g

		return "\n".join(gFlat)



# -todo 111 (decorator, optimize) +0: dramatically slow
	def setTags(self, _name, _tags):
		cEl = self.namedRef[_name]
		for cTag in _tags:
			cEl.set(cTag, _tags[cTag])




# -todo 105 (module-data, filter, API) +0: split to Filter class
	def decorNew(self, _tags, _priority=0):
		return Decorator(_tags, _priority)



	def decorSet(self, _dec, _elA, add=None):
		if add==None:
			_dec.assign(_elA)

		elif add:
			_dec.add(_elA)

		else:
			_dec.sub(_elA)


		toDecorate = Decorator.order(self.namedRef.keys())
		for cName in toDecorate:
			for cDec in toDecorate[cName]:
				self.setTags(cName, cDec.tags)




# SVG tags override class
#  todo 109 (decorator, optimize) +0: too weird entire Decorator flow
class Decorator():
	decorators = []



#Decorators sorted by priority ascending
	def sort():
		levels = sorted(set( [cDec.priority for cDec in Decorator.decorators] ))

		newDec = []

		for cLev in levels:
			for d in Decorator.decorators:
				if d.priority==cLev:
					newDec.append(d)

		Decorator.decorators = newDec



	def __init__(self, _tags, _priority=0):
		self.tags = _tags
		self.priority = _priority
		self.assigned = []
		self.updatedA = []

		Decorator.decorators.append(self)
		Decorator.sort()



	def reset(self):
		self.assigned = []
		self.updatedA = []



	def assign(self, _namesA):
		self.wup( list(_namesA) )



	def add(self, _namesA):
		self.wup( list(set(self.assigned + _namesA)) )



	def sub(self, _namesA):
		self.wup( list(set(self.assigned).difference(_namesA)) )



	def wup(self, _namesA):
		self.updatedA += list( set(self.assigned).symmetric_difference(_namesA) )
		self.assigned = _namesA



	def cdown(self):
		self.updatedA = []



# Get {name:(decorator,)} array, sorted by decorators priority
	def order(_names, all=False):
		upNames = []

		for cDec in Decorator.decorators:
			upNames += cDec.updatedA

			cDec.cdown()


		outDec = {}

		for cName in set(upNames).intersection(_names):
			decList = []
			updated = False

			for cDec in Decorator.decorators:
				if cName in cDec.assigned:
					decList.append(cDec)

					updated = True

			if updated:
				outDec[cName] = decList


		return outDec
