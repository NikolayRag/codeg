'''
Codeg, gcode playground 
https://github.com/NikolayRag/codeg
'''

from Ui import *
from GGData import *
from Dispatch import *
from args import *


#  todo 202 (clean) +0: add app constants
if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()
		
		cDis = Dispatch(cGG)

		cUi = Ui(cArgs, cGG, cDis)
		cUi.exec()


		logging.warning('Exiting')
