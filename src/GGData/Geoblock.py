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
# =todo 128 (mark, optimize, decide) +10: Move marks assignment to geo dict WTF?!
	namedLayers = {}
	namespace = ''



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

			if tagType in [ 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path' ]:
				for cField in Geoblock.CachedFields:
					cTag.set('cache-'+cField, cTag.get(cField) or '')

				cName = tagType +str(i)
				self.namedLayers[cName] = Geolayer(cTag, cName)

				i += 1



	def xmlRoot(self, _string):
		cRoot = self.geoXML.getroot()
		return (XML.tostring(cRoot) if _string else cRoot)



# -todo 111 (mark, optimize) +0: dramatically slow mark reapply
	def getObj(self, _nameA):
		return [self.namedLayers[n] for n in _nameA]



	def names(self):
		return self.namedLayers.keys()



class Geolayer():
	obj = None
	name = ''
	mark = None


	def __init__(self, _obj, _name=''):
		self.obj = _obj
		self.name = _name



	def setTag(self, _tag, _data):
		self.obj.set(_tag, _data)
