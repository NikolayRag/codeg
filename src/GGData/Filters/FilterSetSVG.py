from ..Geofilter import *



class FilterSetSVG(Geofilter):
	name = 'SetSVG'
	step = 'UI'



	def proccess(self, _geo, _data):
		for cTag in self.dataOwn:
			_geo.setTag(cTag, self.dataOwn[cTag], dirty=False)

