from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

from .BindFilter import *



class GeoWidget(QWidget):
	LayerColumnName = 0
	LayerColumnSwitch = 1

	LdataName = Qt.UserRole +0
	LdataItem = Qt.UserRole +1


	defUi = './Ui/GeoWidget.ui'

	eventTypes = None


	sigItemSelect = Signal(object, bool)
	sigItemHover = Signal(object, bool)
	sigItemDataSet = Signal(object, list)
	sigChanged = Signal(bool)

	#runtime

	geoblock = None
	lastHover = None
	lastSelection = []



### PRIVATE 


	def geoitemSet(self, _item, _on):
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



	def itemSelection(self):
		out = {}

		for cRange in self.wListItems.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				out[cRow] = self.wListItems.item(cRow, self.LayerColumnName).data(self.LdataItem)

		return out



	def itemSelect(self, _selection=False):
		if not _selection:
			self.wListItems.clearSelection()

			return


		print(_selection)



	def itemSelected(self):
		cSelection = self.itemSelection().values()


		for cObj in self.lastSelection:
			if cObj not in cSelection:
				self.sigItemSelect.emit(cObj, False)

		for cObj in cSelection:
			if cObj not in self.lastSelection:
				self.sigItemSelect.emit(cObj, True)

		self.lastSelection = cSelection


		self.sigChanged.emit(True)



	def itemHover_(self, _e):
		self.itemHover()


	def itemHover(self, _row=-1, _col=-1):
		if self.lastHover:
			self.sigItemHover.emit(self.lastHover, False)


		if _row >= 0:
			cGItem = self.lastHover = self.wListItems.item(_row, _col).data(self.LdataItem)
			if cGItem:
				self.sigItemHover.emit(cGItem, True)


		self.sigChanged.emit(False)




	def itemClicked(self, _row, _col):
		#blank space click
		if _row == self.wListItems.rowCount()-1:
			self.wListItems.clearSelection()
			return
			

		if _col == self.LayerColumnSwitch:
			cGItem = self.wListItems.item(_row, _col).data(self.LdataItem)

			cSelection = self.itemSelection()


			#explicit single item select
			if _row not in cSelection.keys():
				self.wListItems.selectRow(_row)
				cSelection = {_row: cGItem}


			newState = not cGItem.dataGet('visible', True)
			self.itemsSwitchVis(cSelection, newState)


		self.sigChanged.emit(False)



	def itemsSwitchVis(self, _cSelection, _newState):
# =todo 114 (module-ui, fix) +0: change vis for select-all case
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection

		for cRow, cGItem in _cSelection.items():
			#skip items already set in a group
			if _newState == cGItem.dataGet('visible'):
				continue


			cItem = self.wListItems.item(cRow, self.LayerColumnSwitch)
			self.geoitemSet(cItem, _newState)

			cGItem.dataSet({'visible':_newState})
			self.sigItemDataSet.emit(cGItem, ['visible'])



	def __init__(self, _geoblock=None):
		QWidget.__init__(self)


		loadUi = QUiLoader().load(self.defUi)
		self.setLayout(loadUi.layout())


		self.wListItems = self.findChild(QTableWidget, "listItems")

		self.wListItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.wListItems.itemSelectionChanged.connect(self.itemSelected)
		self.wListItems.cellEntered.connect(self.itemHover)

		self.tmpFilter = BindFilter({
			QEvent.Type.Leave: self.itemHover_ })
		self.wListItems.installEventFilter(self.tmpFilter)

		self.wListItems.cellClicked.connect(self.itemClicked)



		if _geoblock:
			self.replace(_geoblock)



	def clean(self):
		self.wListItems.setRowCount(0)



	def replace(self, _geoblock):
		self.clean()

		self.geoblock = _geoblock


		for cItem in self.geoblock.getGeo():
			self.geoitemAdd(cItem)

		#blank
		self.geoitemAdd()


	def getItems(self, selected=False):
		if selected:
			return list(self.lastSelection)


		return list(self.geoblock.getGeo())
