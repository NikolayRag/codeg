import Ui
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		Ui.Ui(cArgs)
