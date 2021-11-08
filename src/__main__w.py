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
	'Application': {
		'initFit': [0.85],
		'scheme': ['dark', True, 'Style scheme'],

		'wSize': [None],
		'wMaxi': [False],
	},
	'Viewport': {
		'fit': [0.7, True, 'Fit ratio'],
		'fitGeo': [.5, True, 'Fit geometry ratio'],
		'offsetX': [0.66, True, 'Fit center'],

		'panMargins': [.2, True, 'Pan limit margins'],
		'scaleMin': [10],
		'scaleMax': [1000],
		'spotDist': [3, True, "Mouse interaction \nspot size"],
		'zoomStep': [1.1, True, 'Mouse wheel zoom multiplier'],
	},
	'Ui': {
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
