'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

from Ui import *
from GGData import *
from Dispatch import *
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()
		cDis = Dispatch(cGG)


		cUi = Ui(cArgs, cGG)
		cUi.setUICB(cDis.getDevices, cDis.runDevice)


		cUi.go()


		logging.warning('Exiting')
		cArgs.save()

