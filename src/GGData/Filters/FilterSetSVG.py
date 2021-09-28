from ..Geofilter import *



class FilterSetSVG(Geofilter):
	name = 'SetSVG'
	step = 'UI'



	def run(self, _geo, _data):
		for cTag in self.dataOwn:
			_geo.setTag(cTag, self.dataOwn[cTag], dirty=False)
