from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *


class PrefsWidget():
	defUi = './Ui/PrefsWidget.ui'



	def __init__(self, _parent, _blocks):

		self.prefsUi = QUiLoader().load(self.defUi, _parent)
		self.prefsUi.setWindowTitle('Codeg prefs')

		wLayPrefs = self.prefsUi.findChild(QLayout, "layPrefs")


		for arg in _blocks:
			wForm = QFormLayout()

			flag = False
			for prefN, prefV in arg._getData().items():
				if not prefV:
					continue
				flag = True


				fieldVal = QLineEdit(str(getattr(arg, prefN)))
				wForm.addRow(prefV[2], fieldVal)


			if flag:
				wGroup = QGroupBox(arg._getName())
				wGroup.setLayout(wForm)
				wLayPrefs.addWidget(wGroup)



	def exec(self):
		if not self.prefsUi.exec():
			return
