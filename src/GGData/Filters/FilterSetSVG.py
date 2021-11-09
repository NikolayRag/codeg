from ..Markfilter import *



class FilterSetSVG(Markfilter):
	step = 'UI'



	def run(self, _geo, _data):
		for cTag in _data:
			_geo.setTag(cTag, _data[cTag], dirty=False)
