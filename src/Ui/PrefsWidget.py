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


				fieldVal = QLineEdit(str(getattr(arg, prefN)))
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
				setattr(cBock, fieldN, cType(fieldV.text()))


		return True
