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
		'initFit': 0.85,
		'scheme': 'dark',
	},
	'viewport': {
		'fit': 0.7,
		'fitGeo': .5,
		'offsetX': 0.66,
	}
}
AppFields = {
	'app': {
		'wSize': None,
		'wMaxi': False,
	},
	'ui': {
		"recentProject": [],
		"recentLoaded": [],
		"recentSaved": [],
	}
}



if __name__ == '__main__':
	Args(AppPrefs, AppFields, AppName)

	cGG = GGData()
	
	cDis = Dispatch(cGG)

	cUi = Ui(cGG, cDis)
	cUi.exec()


	logging.warning('Exiting')
