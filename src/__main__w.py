'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

from Ui import *
from GGData import *
from Dispatch import *
from Args import *



AppName = 'codeg'
AppPrefs = { #Blockname: {property:[default, range, type, description],..}
	'Application': {
		'initFit': [0.85],
		'scheme': ['dark', ['dark','light'], str, 'Style scheme'],

		'wSize': [None],
		'wPos': [None],
		'wMaxi': [False],
	},
	'Device': {
		'width': [300, [0.,10000], float, 'Default Width'],
		'height': [200, [0.,10000], float, 'Default Height'],
		'GRBLbps': ['115200', ['9600', '115200'], str, 'GRBL bitrate'],
		'last': ['Mockup'],
	},
	'Viewport': {
		'fit': [0.7, [0.,1], float, 'Fit ratio'],
		'fitGeo': [.5, [0,1], float, 'Fit geometry ratio'],
		'offsetX': [0.66, [0,1], float, 'Fit center'],

		'panMargins': [.2, [0,.5], float, 'Pan limit margins'],
		'scaleMin': [10],
		'scaleMax': [1000],
		'spotDist': [3, [0,30], int, "Mouse starting spot size"],
		'zoomStep': [1.1, [1,2], float, 'Mouse wheel zoom multiplier'],
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


	fallbackSize = (Args.Device.width, Args.Device.height)
	deviceDefs = {
		'EngineArduinoGRBL': {'rate':int(Args.Device.GRBLbps)},
	}
	cDis = DispatchManager(size=fallbackSize, definitions=deviceDefs)


	cUi = Ui(cGG, fallbackSize, dispatch=cDis)
	cUi.exec()


	logging.warning('Exiting')
