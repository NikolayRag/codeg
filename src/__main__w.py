'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

# =todo 17 (spec, module-dispatch) +0: send to serial-usb (arduino)
#todo

from Ui import *
from GGData import *
from Dispatch import *
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()
		cDis = Dispatch(cGG)


		cUi = Ui(cArgs)
		cUi.setUICB(cGG.loadXML, cGG.saveG, cDis.getDevices)


		cUi.go()


		logging.warning('Exiting')
		cArgs.save()

