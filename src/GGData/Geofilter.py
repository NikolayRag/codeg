'''
Applied to Geoblock by Geomark, 
'''

class Geofilter():
	filterCB = None



	def __init__(self, _filterCB):
		self.filterCB = _filterCB



	def filtered(self, _geo):
		return filterCB(_geo) if filterCB else _geo





class FilterSetSVG(Geofilter):

	def __init__(self, _filterCB):
		Geofilter.__init__(self, _filterCB)



# -todo 111 (mark, optimize) +0: dramatically slow apply
	def setTags(self, _name, _tags):
		cEl = self.geoNamed[_name]

		for cTag in _tags:
			cEl.set(cTag, _tags[cTag])
