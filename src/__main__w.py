#  todo 9 (spec, module-data) +0: operate project data
#  todo 10 (spec, module-data) +0: operate scene data
#  todo 11 (spec, module-data) +0: read/save own format
# -todo 7 (spec, module-data) +0: read svg
#  todo 8 (spec, module-data) +0: save gcode

# =todo 12 (spec, module-ui) +1: show scene
# =todo 13 (spec, module-ui, proto) +0: render from xml svg
#  todo 15 (spec, module-ui, viewport) +0: basic mouse zoom, pan and reset
#  todo 16 (spec, module-ui) +0: layers
#  todo 14 (spec, module-ui) +0: render from module-data

# =todo 17 (spec, module-dispatch, proto) +0: send to serial-usb (arduino)
#  todo 18 (spec, module-data) +0: standalone dispatcher codegg
#  todo 19 (spec, module-data) +0: send to codegg

#todo

from Ui import *
from GGData import *
from args import *


if __name__ == '__main__':
	cArgs= Args(True)

	if cArgs.args:
		cGG = GGData()

		cUi = Ui(cArgs)
		cUi.setUICB(cGG.loadXML)


		cUi.go()


		logging.warning('Exiting')
		cArgs.save()

