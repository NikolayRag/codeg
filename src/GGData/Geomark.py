'''
Geometry applied set of data
Holds filter function, filter roadpoint and supply data to be applied
to object layer

Filter roadpoint is one of several known origins:
- at creation/load
- at user explicit action
- at output
'''



# =todo 112 (mark, feature) +0: complex mark
# =todo 124 (filter, module-data) +0: make set svg tag as system filter
#

class Geomark():
# =todo 127 (mark, optimize, decide) +10: Move marks assignment to Geoblock WTF?!
#  todo 126 (mark, optimize) +0: chage to {geo:state} dict

# -todo 129 (mark) +0: store custom fields data list
	markData = None
	markFilter = None
	priority = 0



	def __init__(self, _data, _priority=0, _filter=None):
		self.markData = _data
		self.markFilter = _filter

		self.priority = _priority



	def applyFilter(self, _geo, _step):
		if self.markFilter.step == _step:
			self.markFilter.proccess(_geo, self.markData)
