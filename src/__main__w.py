'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

from Ui import *
from GGData import *
from Dispatch import *
from Args import *



AppName = 'codeg'
AppPrefs = {
	'app': {
		'initFit': [0.85, True],
		'scheme': ['dark', True],

		'wSize': [None],
		'wMaxi': [False],
	},
	'viewport': {
		'fit': [0.7, True],
		'fitGeo': [.5, True],
		'offsetX': [0.66, True],

		'panMargins': [.2, True],
		'scaleMin': [10, True],
		'scaleMax': [1000, True],
		'spotDist': [3, True],
		'zoomStep': [1.1, True],
	},
	'ui': {
		'recentProject': [[]],
		'recentLoaded': [[]],
		'recentSaved': [[]],
	}
}



if __name__ == '__main__':
	Args(AppPrefs, AppName)

	cGG = GGData()
	
	cDis = Dispatch(cGG)

	cUi = Ui(cGG, cDis)
	cUi.exec()


	logging.warning('Exiting')
