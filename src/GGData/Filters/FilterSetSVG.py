from ..Markfilter import *



class FilterSetSVG(Markfilter):
	step = 'UI'



	def run(self, _geo, _data):
		for cTag in self.dataOwn:
			_geo.setTag(cTag, self.dataOwn[cTag], dirty=False)
