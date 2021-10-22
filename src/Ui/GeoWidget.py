from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *



class GeoWidget(QWidget):
	defUi = './Ui/GeoWidget.ui'

	eventTypes = None



	def eventFilter(self, _o, _e):
		if _e.type() in self.eventTypes:
			self.eventTypes[_e.type()](event=_e)

		return False


### PRIVATE 


	def layerSelect(self):
		print('itemSelect')



	def layerHover(self, _row=-1, _col=-1, event=None):
		print('itemHover', _row, _col, event)



	def layerClick(self, _row, _col):
		print('itemClick', _row, _col)



	def __init__(self):
		QWidget.__init__(self)


		loadUi = QUiLoader().load(self.defUi)
		self.setLayout(loadUi.layout())


		self.wListItems = self.findChild(QTableWidget, "listItems")

		self.wListItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.wListItems.itemSelectionChanged.connect(self.layerSelect)
		self.wListItems.cellEntered.connect(self.layerHover)
		self.eventTypes = {QEvent.Type.Leave: self.layerHover}
		self.wListItems.installEventFilter(self)

		self.wListItems.cellClicked.connect(self.layerClick)

