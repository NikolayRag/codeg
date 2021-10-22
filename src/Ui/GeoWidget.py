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
	sigCtrlLayersSet = Signal(list, bool)

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
				cName = self.wListItems.item(cRow, self.LayerColumnName)
				out[cRow] = cName.data(self.LdataName)

		return out



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
		
		if _row == self.wListItems.rowCount()-1:
			self.wListItems.clearSelection()

			return
			

		if _col == self.LayerColumnSwitch:
			self.layersSwitchVis(_row, _col)



	def layersSwitchVis(self, _row, _col):
		cSelection = list(self.layerSelection().keys())
		namesA = []
		newState = not self.wListItems.item(_row, _col).data(self.LdataOn)


		if _row not in cSelection:
			self.wListItems.selectRow(_row)
			cSelection = [_row]


# =todo 114 (module-ui, fix) +0: change vis for select-all case
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection
		for cRow in cSelection:
			cItem = self.wListItems.item(cRow, _col)
			if newState == cItem.data(self.LdataOn):
				continue

			self.geoitemSet(cItem, newState)
			namesA.append( cItem.data(self.LdataName) )


		self.sigCtrlLayersSet.emit(
			namesA,
			newState
		)



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
