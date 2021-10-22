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



	def __init__(self):
		QWidget.__init__(self)


		loadUi = QUiLoader().load(self.defUi)
		self.setLayout(loadUi.layout())


		self.wListGeoItems = self.findChild(QTableWidget, "listGeoItems")

		self.wListGeoItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.wListGeoItems.itemSelectionChanged.connect(self.layerSelect)
		self.wListGeoItems.cellEntered.connect(self.layerHover)
		self.eventTypes = {QEvent.Type.Leave: self.layerHover}
		self.wListGeoItems.installEventFilter(self)

		self.wListGeoItems.cellClicked.connect(self.layerClick)



	def layerSelect(self):
		print('itemSelect')



	def layerHover(self, _row=-1, _col=-1, event=None):
		print('itemHover', _row, _col, event)



	def layerClick(self, _row, _col):
		print('itemClick', _row, _col)
