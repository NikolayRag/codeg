from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *



class GeoWidget(QWidget):
	LayerColumnName = 0
	LayerColumnSwitch = 1

	LdataName = Qt.UserRole +0
	LdataItem = Qt.UserRole +1
	LdataOn = Qt.UserRole +2


	defUi = './Ui/GeoWidget.ui'

	eventTypes = None


	#runtime

	block = None


	def eventFilter(self, _o, _e):
		if _e.type() in self.eventTypes:
			self.eventTypes[_e.type()](event=_e)

		return False


### PRIVATE 


	def geoitemSet(self, _item, _on):
		_item.setData(self.LdataOn, _on)

		c = QColor('#4c4')
		c.setAlpha(255 if _on else 0)
		_item.setBackground(c)



	def geoitemAdd(self, _item=None):
		cRow = self.wListItems.rowCount()

		self.wListItems.insertRow(cRow)

		if _item:
			itemName = QTableWidgetItem(_item.name)
#
			itemName.setData(self.LdataName, _item.name)
#
			itemName.setData(self.LdataItem, _item)
			self.wListItems.setItem(cRow, self.LayerColumnName, itemName)
		
			itemOn = QTableWidgetItem()
#
			itemOn.setData(self.LdataName, _item.name)
#
			itemOn.setData(self.LdataItem, _item)

			itemOn.setFlags(Qt.NoItemFlags)
			visible = _item.dataGet('visible', True)
			self.geoitemSet(itemOn, visible)
			self.wListItems.setItem(cRow, self.LayerColumnSwitch, itemOn)

		else:
			for i in range(self.wListItems.columnCount()):
				cItem = QTableWidgetItem()
				cItem.setFlags(Qt.NoItemFlags)
				self.wListItems.setItem(cRow, i, cItem)



	def layerSelect(self):
		print('itemSelect')



	def layerHover(self, _row=-1, _col=-1, event=None):
		print('itemHover', _row, _col, event)



	def layerClick(self, _row, _col):
		print('itemClick', _row, _col)



	def __init__(self, _geoblock=None):
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



		if _geoblock:
			self.replace(_geoblock)



	def clean(self):
		self.wListItems.setRowCount(0)



	def replace(self, _geoblock):
		self.clean()

		self.block = _geoblock


		for cItem in self.block.getObj():
			self.geoitemAdd(cItem)

		#blank
		self.geoitemAdd()
