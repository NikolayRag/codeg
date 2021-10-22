from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *



class GeoWidget(QWidget):
	defUi = './Ui/GeoWidget.ui'



	def __init__(self):
		QWidget.__init__(self)


		self.lLayout = QVBoxLayout()
		self.lLayout.setSpacing(0)
		self.lLayout.setContentsMargins(0,0,0,0)
		self.setLayout(self.lLayout)


		self.wMain = QUiLoader().load(self.defUi)
		self.lLayout.addWidget(self.wMain)
