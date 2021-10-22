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


	sigLayerSelect = Signal(list)
	sigLayerHover = Signal(str)
	sigItemDataSet = Signal(object, list)
	sigChanged = Signal()

	#runtime

	block = None


	def eventFilter(self, _o, _e):
		if _e.type() in self.eventTypes:
			self.eventTypes[_e.type()](event=_e)

		return False


### PRIVATE 


	def layerSelection(self):
		out = {}

		for cRange in self.wListItems.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				out[cRow] = self.wListItems.item(cRow, self.LayerColumnName).data(self.LdataItem)

		return out



	def geoitemSet(self, _item, _on):
		_item.setData(self.LdataOn, _on)

		c = QColor('#4c4')
		c.setAlpha(255 if _on else 0)
		_item.setBackground(c)


#  todo 193 (ux, widgets, decide) +0: move to GeoItem widget
	def geoitemAdd(self, _geoitem=None):
		cRow = self.wListItems.rowCount()

		self.wListItems.insertRow(cRow)

		if _geoitem:
			itemName = QTableWidgetItem(_geoitem.name)
			itemName.setData(self.LdataItem, _geoitem)
			self.wListItems.setItem(cRow, self.LayerColumnName, itemName)
		
			itemOn = QTableWidgetItem()
			itemOn.setData(self.LdataItem, _geoitem)

			itemOn.setFlags(Qt.NoItemFlags)
			visible = _geoitem.dataGet('visible', True)
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
		#blank space click
		if _row == self.wListItems.rowCount()-1:
			self.wListItems.clearSelection()
			return
			

		if _col == self.LayerColumnSwitch:
			cGeo = self.wListItems.item(_row, _col).data(self.LdataItem)

			cSelection = self.layerSelection()


			#explicit single item select
			if _row not in cSelection.keys():
				self.wListItems.selectRow(_row)
				cSelection = {_row: cGeo}


			newState = not cGeo.dataGet('visible', True)
			self.layersSwitchVis(cSelection, newState)


		self.sigChanged.emit()



	def layersSwitchVis(self, _cSelection, _newState):
# =todo 114 (module-ui, fix) +0: change vis for select-all case
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection

		for cRow, cGeo in _cSelection.items():
			#skip items already set in a group
			if _newState == cGeo.dataGet('visible'):
				continue


			cItem = self.wListItems.item(cRow, self.LayerColumnSwitch)
			self.geoitemSet(cItem, _newState)

			cGeo.dataSet({'visible':_newState})
			self.sigItemDataSet.emit(cGeo, ['visible'])



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
