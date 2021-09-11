import xml.etree.ElementTree as XML
import re


class Geoblock():
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


	geoXML = None
	geoNamed = None



	def __init__(self, _source, _type):
		self.geoXML = XML.parse(_source)
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
				for cField in Geoblock.CachedFields:
					cTag.set('cache-'+cField, cTag.get(cField) or '')

				cTag.set('id', tagType +str(i))
				self.geoNamed[tagType +str(i)] = cTag

				i += 1



	def xmlRoot(self, _string):
		cRoot = self.geoXML.getroot()
		return (XML.tostring(cRoot) if _string else cRoot)



# -todo 111 (decorator, optimize) +0: dramatically slow
	def setTags(self, _name, _tags):
		cEl = self.geoNamed[_name]

		for cTag in _tags:
			cEl.set(cTag, _tags[cTag])


	def names(self):
		return self.geoNamed.keys()
