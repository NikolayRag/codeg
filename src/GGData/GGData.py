# -todo 189 (module-data, api, decide) +1: make all indirect (by id) controls
# =todo 90 (ux, module-ui, fix) +5: respect units - both svg and device

#  todo 201 (geo, feature) +0: update reference geometry 


#  todo 25 (module-data, formats) +0: load .nc gcode

'''
Data scope:
	(Filter,)
	(Scene,)
		(Mark,)
			*Filter link
		(Geoblock/(Geo,),)
			*Mark link

'''


from .Scene import *
from .Mark import *
from .Markfilter import *
from .Filters import *



class GGData():

	allFilters = {}
	allScenes = {}

	maxMarkPriority = 0


	def __init__(self):
		self.allFilters = {a.__name__:a for a in Markfilter.__subclasses__()}



	def sceneRemove(self, _name):
		if _name in self.allScenes:
			del self.allScenes[_name]



	def sceneGet(self, _name=''):
		if _name not in self.allScenes:
			self.allScenes[_name] = Scene(_name)

		return self.allScenes[_name]



	def sceneList(self):
		return dict(self.allScenes)



###


#	Only create Mark with given Markfilter and data.
#	Should be appended to scene explicitely by Scene.markAppend().
	def markNew(self, data={}, filterName=None, filterData={}, priority=None):
		if priority==None:
			priority = self.maxMarkPriority +1

		self.maxMarkPriority = priority


		filterProc = None

		if filterName:
			if filterName not in self.allFilters:
				print('Warning: filter', filterName, 'is unknown')

				newclass = type(filterName, (Markfilter,), {})
				self.allFilters[filterName] = newclass


			filterProc = self.allFilters[filterName](filterData)


		cMark = Mark(data, priority, filterProc)
		return cMark
