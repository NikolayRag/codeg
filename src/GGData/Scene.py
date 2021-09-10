# =todo 9 (scene, spec, module-data) +1: operate project data
# =todo 113 (scene, module-ui, ux) +0: assignable layer decorator marks holding control data
# =todo 93 (scene, feature) +0: store scene layer and layout state
#  todo 92 (feature) +0: multiple sources scene


import xml.etree.ElementTree as XML
import re


class Scene():
	# Should contain fields affected by Decorators
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


	decorators = None



	def __init__(self, _defDecs=[]):
		self.decorators = []


		for cDec in _defDecs:
			cDec.reset()

			self.decoratorAdd(cDec)



	def decoratorReapply(self):
		toDecorate = self.decoratorsOrder(self.geoNamed.keys())
		for cName in toDecorate:
			for cDec in toDecorate[cName]:
				self.setTags(self.geoNamed[cName], cDec.tags)



# -todo 111 (decorator, optimize) +0: dramatically slow
	def setTags(self, _el, _tags):
		for cTag in _tags:
			_el.set(cTag, _tags[cTag])



	def decoratorAdd(self, _newDec):
		decList = self.decorators + [_newDec]
		levels = sorted(set( [cDec.priority for cDec in decList] ))

		newDecSorted = []

		for cLev in levels:
			for d in decList:
				if d.priority==cLev:
					newDecSorted.append(d)

		self.decorators = newDecSorted



# Get {name:(decorator,)} array, sorted by decorators priority
	def decoratorsOrder(self, _namesLimit):
		upNames = []

		for cDec in self.decorators:
			upNames += cDec.updatedA

			cDec.cdown()


		outDec = {}

		for cName in set(upNames).intersection(_namesLimit):
			decList = []
			updated = False

			for cDec in self.decorators:
				if cName in cDec.assigned:
					decList.append(cDec)

					updated = True

			if updated:
				outDec[cName] = decList


		return outDec


### GEO ###


	def geoAdd(self, _geo):
		self.geoXML = _geo
		self.geoNamed = {}


		i = 1
		for cTag in self.geoXML.iter():
			tagType = cTag.tag[28:]

			if tagType == 'xml':
				None

#  todo 82 (module-data, ux) +0: parse groups
			if tagType == 'g':
				None

			if tagType in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in Scene.CachedFields:
					cTag.set('cache-'+cField, cTag.get(cField) or '')

				cTag.set('id', tagType +str(i))
				self.geoNamed[tagType +str(i)] = cTag

				i += 1



	def geoMeta(self):
		return {cN:{'on':True} for cN in self.geoNamed}



	def getSceneXML(self, toString=False):
		cRoot = self.geoXML.getroot()
		return (XML.tostring(cRoot) if toString else cRoot)
