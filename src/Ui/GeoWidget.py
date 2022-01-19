from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

from .BindFilter import *

# -todo 360 (feature, ux, v2) +0: Unsolo (normal) mode
# =todo 220 (ux, widget) +0: make Geoitems list view continuous
# =todo 318 (ux, widget, geo) +5: scale control
# =todo 319 (ux, widget, geo) +0: rotate control


class GeoWidgetItems(QWidget):
	iconVis = QIcon('./resource/vis.svg')
	iconVis.addFile('./resource/vis.svg', mode=QIcon.Disabled)
	iconInvis = QIcon('./resource/invis.svg')
	iconInvis.addFile('./resource/invis.svg', mode=QIcon.Disabled)

	LayerColumnName = 0
	LayerColumnSwitch = 1

	LdataName = Qt.UserRole +0
	LdataItem = Qt.UserRole +1


	defUi = './Ui/GeoWidget.ui'

	eventTypes = None


	sigItemSelect = Signal(object, bool)
	sigItemHover = Signal(object, bool)
	sigItemDataSet = Signal(object, list)
	sigTouched = Signal()
	sigSelected = Signal(list)

	#runtime

	lastHover = None
	lastSelection = []

	itemRef = {}


### PRIVATE 


	def geoitemSet(self, _item, _on):
		_item.setIcon(self.iconVis if _on else self.iconInvis)



#  todo 193 (ux, widgets, decide) +0: move to GeoItem widget
	def geoitemAdd(self, _geoitem=None):
		cRow = self.wListItems.rowCount()

		self.wListItems.insertRow(cRow)

		if _geoitem:
			itemName = QTableWidgetItem(_geoitem.name)
			itemName.setData(self.LdataItem, _geoitem)
			self.wListItems.setItem(cRow, self.LayerColumnName, itemName)
		
	
			ctrlVisible = QTableWidgetItem()
			ctrlVisible.setData(self.LdataItem, _geoitem)

			ctrlVisible.setFlags(Qt.NoItemFlags)
			visible = _geoitem.dataGet('visible', True)
			self.geoitemSet(ctrlVisible, visible)
			self.wListItems.setItem(cRow, self.LayerColumnSwitch, ctrlVisible)

			if _geoitem.dataGet('selected', False):
				self.wListItems.setCurrentItem(itemName, QItemSelectionModel.Select)

			self.itemRef[_geoitem] = itemName

		else:
			for i in range(self.wListItems.columnCount()):
				cItem = QTableWidgetItem()
				cItem.setFlags(Qt.NoItemFlags)
				self.wListItems.setItem(cRow, i, cItem)



	def itemSelection(self):
		out = {}

		for cRange in self.wListItems.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cItem = self.wListItems.item(cRow, self.LayerColumnName).data(self.LdataItem)
				if cItem:
					out[cRow] = cItem


		return out



	def itemSelectSet(self, _selection=[], _outside=True):
		if _outside:
			self.wListItems.blockSignals(True)

			self.wListItems.clearSelection()

			for cEl in _selection:
				self.wListItems.setCurrentItem(self.itemRef[cEl], QItemSelectionModel.Select)

			self.wListItems.blockSignals(False)


		for cObj in self.lastSelection:
			if cObj not in _selection:
				self.sigItemSelect.emit(cObj, False)

		for cObj in _selection:
			if cObj not in self.lastSelection:
				self.sigItemSelect.emit(cObj, True)

		self.lastSelection = _selection


		self.sigTouched.emit()
		self.sigSelected.emit(list(_selection))



	def itemSelected(self):
		cSelection = self.itemSelection().values()

		self.itemSelectSet(cSelection, False)



	def itemHover(self, _row=-1, _col=-1):
		if self.lastHover:
			self.sigItemHover.emit(self.lastHover, False)


		if _row >= 0:
			cGItem = self.lastHover = self.wListItems.item(_row, _col).data(self.LdataItem)
			if cGItem:
				self.sigItemHover.emit(cGItem, True)


		self.sigTouched.emit()




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


		self.sigTouched.emit()



	def itemsSwitchVis(self, _cSelection, _newState):
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection

		for cRow, cGItem in _cSelection.items():
			#skip items already set in a group
			if _newState == cGItem.dataGet('visible'):
				continue


			cItem = self.wListItems.item(cRow, self.LayerColumnSwitch)
			self.geoitemSet(cItem, _newState)

			cGItem.dataSet({'visible':_newState})
			self.sigItemDataSet.emit(cGItem, ['visible'])



	def __init__(self, _geoblock):
		QWidget.__init__(self)


		self.itemRef = {}


		loadUi = QUiLoader().load(self.defUi)
		self.setLayout(loadUi.layout())


		self.wListItems = self.findChild(QTableWidget, "listItems")
		self.wListItems.setIconSize(QSize(14,14))

		self.wListItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.wListItems.itemSelectionChanged.connect(self.itemSelected)
		self.wListItems.cellEntered.connect(self.itemHover)

		self.tmpFilter = BindFilter({
			QEvent.Type.Leave: lambda e: self.itemHover() })
		self.wListItems.installEventFilter(self.tmpFilter)

		self.wListItems.cellClicked.connect(self.itemClicked)


		#add
		for cItem in _geoblock.getGeo():
			self.geoitemAdd(cItem)

		#blank
		self.geoitemAdd()



	def getSelection(self):
		return list(self.lastSelection)





class GeoWidget(QListWidget):
	LdataWidget = Qt.UserRole +0
	LdataBlock = Qt.UserRole +1
	LdataData = Qt.UserRole +2


	sigItemSelect = Signal(object, bool)
	sigItemHover = Signal(object, bool)
	sigItemDataSet = Signal(object, list)
	sigTouchRun = Signal(bool)
	sigTouched = Signal(object, object)
	sigSelected = Signal(list)
	sigActivate = Signal(object, bool)


	contItems = None

	lastEntry = None



	def __init__(self, _contBlocks, _contItems):
		QListWidget.__init__(self)

		self.setFrameShape(QFrame.NoFrame)
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
		self.setMinimumHeight(80)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		_contBlocks.addWidget(self)

		self.contItems = _contItems

		self.itemClicked.connect(self.currentSet)



	def blockAdd(self, _geoblock, _data):
		cWidget = GeoWidgetItems(_geoblock)

		cWidget.sigItemSelect.connect(lambda item, state: self.sigItemSelect.emit(item, state) )
		cWidget.sigItemHover.connect(lambda item, state: self.sigItemHover.emit(item, state) )
		cWidget.sigItemDataSet.connect(lambda item, names: self.sigItemDataSet.emit(item, names) )
		cWidget.sigTouched.connect(lambda: self.sigTouched.emit(_geoblock, _data) )
		cWidget.sigSelected.connect(lambda items: self.sigSelected.emit(items) )


		cBlockItem = QListWidgetItem(_geoblock.label())
		cBlockItem.setData(self.LdataWidget, cWidget)
		cBlockItem.setData(self.LdataBlock, _geoblock)
		cBlockItem.setData(self.LdataData, _data)

		self.addItem(cBlockItem)
		self.contItems.addWidget(cWidget)


		self.currentSet(cBlockItem)



	def currentSet(self, _entry):
		self.sigTouchRun.emit(True)


		self.removeLast()

		self.setCurrentItem(_entry)
		cItems = _entry.data(self.LdataWidget)
		cItems.show()


		cBlock = _entry.data(self.LdataBlock)
		self.sigActivate.emit(cBlock, True)
		self.sigTouched.emit(cBlock, _entry.data(self.LdataData))
		self.sigSelected.emit(list(cItems.itemSelection().values()))


		self.sigTouchRun.emit(False)
		self.lastEntry = _entry



	def removeLast(self):
		if cItem := self.lastEntry:
			cItem.data(self.LdataWidget).hide()

			cBlock = cItem.data(self.LdataBlock)
			self.sigActivate.emit(cBlock, False)
			self.sigTouched.emit(cBlock, cItem.data(self.LdataData))


		self.sigSelected.emit([])



	def clean(self):
		self.removeLast()

		self.clear()

		self.lastEntry = None



	def currentSelection(self):
		if not self.lastEntry:
			return []


		cWidget = self.lastEntry.data(self.LdataWidget)
		return cWidget.getSelection()



	def selectGeo(self, _items=[]):
		if not self.lastEntry:
			return


		self.sigTouchRun.emit(True)

		cWidget = self.lastEntry.data(self.LdataWidget)
		cWidget.itemSelectSet(_items)

		self.sigTouchRun.emit(False)



	#returns {Geoblock: SvgDescriptor} dict
	def getBlocks(self, _all=False):
		cList = [self.lastEntry] if self.lastEntry else []


		if _all:
			cList = []
			for i in range(self.count()):
				cList.append( self.item(i) )


		out = {}
		for cItem in cList:
			out[cItem.data(self.LdataBlock)] = cItem.data(self.LdataData)


		return out
