from Ui import *
from GGData import *
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()

		cUi = Ui(cArgs)
		cUi.setUICB(cGG.cbUIFileLoad)


		cUi.go()


		logging.warning('Exiting')
		cArgs.save()

