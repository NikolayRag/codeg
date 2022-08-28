from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

# -todo 246 (widget, feature) +0: add reset settings

class PrefsWidget():
	defUi = './Ui/PrefsWidget.ui'

	links = {}



	def __init__(self, _parent, _blocks):

		self.prefsUi = QUiLoader().load(self.defUi, _parent)
		self.prefsUi.setWindowTitle('Codeg prefs')

		wLayPrefs = self.prefsUi.findChild(QLayout, "layPrefs")


		for cArg in _blocks:
			wForm = QFormLayout()


			blockDict = {}

			for prefN, prefV in cArg._getData().items():
				if not prefV:
					continue


				cVal = getattr(cArg, prefN)
				cData = cArg._getData()[prefN][0]


				fieldVal = fieldW = None

				if prefV[1] == str:
					if type(cData) == list:
						fieldW = QComboBox()
						for opt in cData:
							fieldW.addItem(opt)

						if cVal in cData:
							fieldW.setCurrentIndex(cData.index(cVal))


					else:
						fieldW = QLineEdit(cVal)


				def spinslide(spin, slide, mul):
					slide.valueChanged.connect(lambda v: spin.setValue(v/mul))
					spin.valueChanged.connect(lambda v: slide.setValue(v*mul))

				if prefV[1] == float or prefV[1] == int:
					floatMul = 100 if prefV[1]==float else 1

					fieldSpinner = QDoubleSpinBox() if prefV[1]==float else QSpinBox()
					fieldSpinner.setMinimumWidth(40)
					fieldSpinner.setMaximumWidth(40)
					fieldSpinner.setButtonSymbols(QAbstractSpinBox.NoButtons)
					fieldSpinner.setRange(cData[0], cData[1])
					fieldSpinner.setValue(cVal)
					fieldSpinner.setSingleStep(.05 if prefV[1]==float else 1)

					fieldVal = QSlider(Qt.Horizontal)
					fieldVal.setRange(cData[0]*floatMul, cData[1]*floatMul)
					fieldVal.setValue(cVal*floatMul)

					spinslide(fieldSpinner, fieldVal, floatMul)

					fieldW = QHBoxLayout()
					fieldW.addWidget(fieldSpinner)
					fieldW.addWidget(fieldVal)


				if prefV[1] == bool:
					fieldW = QCheckBox()
					fieldW.setCheckState(Qt.Checked if cVal else Qt.Unchecked)


				wForm.addRow(prefV[2], fieldW)

				blockDict[prefN] = fieldVal or fieldW


			if blockDict:
				wGroup = QGroupBox(cArg._getName())
				wGroup.setLayout(wForm)
				wLayPrefs.addWidget(wGroup)


			self.links[cArg] = blockDict



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

				elif cType==str:
					if type(fieldV) == QComboBox:
						fieldV = fieldV.currentText()

					else:
						fieldV = fieldV.text()

				else:
					print('Unknown pref type:', fieldN, cType)
					cType = None

				
				if cType:
					setattr(cBock, fieldN, cType(fieldV))


		return True
