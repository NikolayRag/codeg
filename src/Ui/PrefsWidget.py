from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *


class PrefsWidget():
	defUi = './Ui/PrefsWidget.ui'

	links = {}



	def __init__(self, _parent, _blocks):

		self.prefsUi = QUiLoader().load(self.defUi, _parent)
		self.prefsUi.setWindowTitle('Codeg prefs')

		wLayPrefs = self.prefsUi.findChild(QLayout, "layPrefs")


		for arg in _blocks:
			wForm = QFormLayout()


			blockDict = {}

			for prefN, prefV in arg._getData().items():
				if not prefV:
					continue


				cVal = getattr(arg, prefN)
				cData = arg._getData()[prefN][0]


				if prefV[1] == str:
					if type(cData) == list:
						fieldVal = QComboBox()
						for opt in cData:
							fieldVal.addItem(opt)

						if cVal in cData:
							fieldVal.setCurrentIndex(cData.index(cVal))


					else:
						fieldVal = QLineEdit(cVal)


				if prefV[1] == float or prefV[1] == int:
					floatMul = 100 if prefV[1]==float else 1

					fieldVal = QSlider(Qt.Horizontal)
					fieldVal.setRange(cData[0]*floatMul, cData[1]*floatMul)
					fieldVal.setValue(cVal*floatMul)


				if prefV[1] == bool:
					fieldVal = QCheckBox()
					fieldVal.setCheckState(Qt.Checked if cVal else Qt.Unchecked)



				wForm.addRow(prefV[2], fieldVal)

				blockDict[prefN] = fieldVal


			if blockDict:
				wGroup = QGroupBox(arg._getName())
				wGroup.setLayout(wForm)
				wLayPrefs.addWidget(wGroup)


			self.links[arg] = blockDict



	def exec(self):
		if not self.prefsUi.exec():
			return


		for cBock, fields in self.links.items():
			for fieldN, fieldV in fields.items():
				cType = cBock._getData()[fieldN][1]

				if cType==float:
					fieldV = fieldV.value() *.01
				elif cType==int:
					fieldV = fieldV.value()

				elif cType==bool:
					fieldV = fieldV.checkState() == Qt.Checked

				elif type(fieldV) == QComboBox:
					fieldV = fieldV.currentText()

				else:
					fieldV = fieldV.text()

				setattr(cBock, fieldN, cType(fieldV))


		return True
