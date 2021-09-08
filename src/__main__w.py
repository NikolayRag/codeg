'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

from Ui import *
from GGData import *
from Dispatch import *
from args import *


#  todo 92 (feature) +0: multiple sources scene
# =todo 113 (module-ui, ux) +0: assignable layer decorator marks holding control data
# =todo 93 (feature) +0: store scene layer and layout state
if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()
		cDis = Dispatch(cGG)


		cUi = Ui(cArgs, cGG, cDis)

		cUi.exec()


		logging.warning('Exiting')
