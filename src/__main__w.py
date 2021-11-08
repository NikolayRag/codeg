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
		'scheme': ['dark', True, str, 'Style scheme'],

		'wSize': [None],
		'wMaxi': [False],
	},
	'Viewport': {
		'fit': [0.7, True, float, 'Fit ratio'],
		'fitGeo': [.5, True, float, 'Fit geometry ratio'],
		'offsetX': [0.66, True, float, 'Fit center'],

		'panMargins': [.2, True, float, 'Pan limit margins'],
		'scaleMin': [10],
		'scaleMax': [1000],
		'spotDist': [3, True, float, "Mouse interaction \nspot size"],
		'zoomStep': [1.1, True, float, 'Mouse wheel zoom multiplier'],
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
