# =todo 17 (spec, module-dispatch, proto) +0: send to serial-usb (arduino)

#todo

from Ui import *
from GGData import *
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()

		cUi = Ui(cArgs)
		cUi.setUICB(cGG.loadXML, cGG.saveG)


		cUi.go()


		logging.warning('Exiting')
		cArgs.save()

