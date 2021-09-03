#  todo 33 (module-ui, widgets) +0: zoom slider
#  todo 34 (module-ui, widgets) +0: transform reset


import os, logging
import webbrowser

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

from .SvgViewport import *



class BindFilter(QObject):
	eType = None
	cb = None


	def __init__(self, _etypes, _cb):
		QObject.__init__(self)

		if not hasattr(_etypes, '__iter__'):
			_etypes = (_etypes,)
		self.eTypes = _etypes
		self.cb = _cb


	def eventFilter(self, _o, _e):
		if _e.type() in self.eTypes:
			self.cb(event=_e)

		return False



class AppWindow(QObject):
	LayerColumnName = 0
	LayerColumnSwitch = 1

	LdataName = Qt.UserRole +0
	LdataOn = Qt.UserRole +1

	sigResize = Signal(QSize, bool)
	sigAddFile = Signal()
	sigStoreG = Signal()
	sigDispatch = Signal(str)
	sigLayerSelect = Signal(list)
	sigLayerHover = Signal(str)
	sigCtrlLayersSet = Signal(list, bool)


	aboutHref = "https://github.com/NikolayRag/codeg"

	defaultFit = 0.8



	def __init__(self, _uiFile, _styleFile=None):
		QObject.__init__(self)

		cMain = self.lMain = QUiLoader().load(_uiFile)


		if _styleFile:
			with open(_styleFile) as fQss:
				cMain.setStyleSheet(fQss.read())


		cMain.setWindowTitle('codeg');
		self.tmpFilterWindowResize = BindFilter(
			(QEvent.Type.Resize, QEvent.Type.WindowStateChange),
			self.resized
		)
		cMain.installEventFilter(self.tmpFilterWindowResize)


		#widgets time
		self.lListLayers = cMain.findChild(QTableWidget, "listLayers")

		self.lListLayers.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.lListLayers.itemSelectionChanged.connect(self.layerSelect)
		self.lListLayers.cellEntered.connect(self.layerHover)
		self.tmpFilterLayersLeave = BindFilter(QEvent.Type.Leave, self.layerHover)
		self.lListLayers.installEventFilter(self.tmpFilterLayersLeave)

		self.lListLayers.cellClicked.connect(self.layerClick)

		
		self.lCheckLayerOn = cMain.findChild(QLineEdit, "checkLayerOn")


		self.lLineLayerPower = cMain.findChild(QLineEdit, "lineLayerPower")
		self.lLineLayerPower.setValidator( QIntValidator(0,1000) );


		holderViewport = cMain.findChild(QWidget, "wViewport")
		self.lViewport = SvgViewport(holderViewport)
		self.lViewport.setGrid('resource\\grid.svg')
		self.lViewport.lower()
		self.lViewport.show()

		self.tmpFilterViewResize = BindFilter(
			QEvent.Type.Resize,
			lambda event: self.lViewport.resize(event.size())
		)
		holderViewport.installEventFilter(self.tmpFilterViewResize)


		self.lBtnFit = cMain.findChild(QWidget, "btnFit")

		self.lBtnCaption = cMain.findChild(QWidget, "btnCaption")
		self.lBtnOpen = cMain.findChild(QWidget, "btnLoad")
		self.lBtnStore = cMain.findChild(QWidget, "btnSave")

		self.lFrameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.lFrameDispatcher.setVisible(False)
#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.lDdPorts = cMain.findChild(QWidget, "ddPorts")
		self.lBtnProccess = cMain.findChild(QWidget, "btnProccess")
		self.lLogDev = cMain.findChild(QTextEdit, "logDev")


		self.lBtnFit.clicked.connect(lambda: self.lViewport.canvasFit(self.defaultFit))
		self.lBtnCaption.clicked.connect(self.about)
		self.lBtnOpen.clicked.connect(self.sigAddFile)
		self.lBtnStore.clicked.connect(self.sigStoreG)
		self.lBtnProccess.clicked.connect(self.dispatchRun)



	def show(self):
		self.lMain.show()



	def resize(self, _size, maximize=None):
		self.lMain.resize(
			QSize(*_size)
			if _size else
			QApplication.primaryScreen().size() *.8
		)

		if maximize:
			self.lMain.showMaximized()



### PRIVATE ###



#  todo 79 (module-ui, ux, fix) +0: make size ignored on maximize
	def resized(self, event):
		wSize = self.lMain.size()
		self.sigResize.emit(
			wSize,
			self.lMain.isMaximized()
		)



	def about(self):
		webbrowser.open(self.aboutHref)



#  todo 3 (feature, file) +0: allow picking from Recent files list
	def reactAddFile(self, _data):
		self.lBtnStore.setEnabled(True)
		self.lBtnProccess.setEnabled(True)

		self.lViewport.canvasReset()
		self.lViewport.canvasAdd(_data['xml'])
		self.lViewport.canvasFit(self.defaultFit)


		cList = self.lListLayers
		cList.setRowCount(0)

		cMeta = _data['meta']
		for cName in cMeta:
			self.layerAddItem(cList, cMeta, cName)

		#blank
		self.layerAddItem(cList)



#  todo 20 (module-ui, error) +0: handle errors, maybe status string
	def reactStoreG(self):
		None



	def canvasUpdate(self, _xml):
		self.lViewport.canvasUpdate(_xml)



######### LAYERS #########

	def layerSetItem(self, _item, _on):
		_item.setData(self.LdataOn, _on)

		c = QColor('#4c4')
		c.setAlpha(255 if _on else 0)
		_item.setBackground(c)



	def layerAddItem(self, _list, _meta=None, _name=None):
		cRow = _list.rowCount()

		_list.insertRow(cRow)

		if _meta:
			itemName = QTableWidgetItem(_name)
			itemName.setData(self.LdataName, _name)
			_list.setItem(cRow, self.LayerColumnName, itemName)
		
			itemOn = QTableWidgetItem()
			itemOn.setData(self.LdataName, _name)

			itemOn.setFlags(Qt.NoItemFlags)
			self.layerSetItem(itemOn, _meta[_name]['on'])
			_list.setItem(cRow, self.LayerColumnSwitch, itemOn)

		else:
			for i in range(_list.columnCount()):
				cItem = QTableWidgetItem()
				cItem.setFlags(Qt.NoItemFlags)
				_list.setItem(cRow, i, cItem)



	def layerSelection(self):
		cacheSelection = []

		for cRange in self.lListLayers.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cacheSelection.append(cRow)

		return cacheSelection



	def layerSelect(self):
		selectionNamesA = []

		for cRow in self.layerSelection():
			cName = self.lListLayers.item(cRow, self.LayerColumnName)
			selectionNamesA.append( cName.data(self.LdataName) )


		self.sigLayerSelect.emit(selectionNamesA)



	def layerHover(self, _row=-1, _col=-1, event=None):
		hoverName = None
		if _row >= 0:
			hoverName = self.lListLayers.item(_row, self.LayerColumnName).data(self.LdataName)


		self.sigLayerHover.emit(hoverName)



	def layerClick(self, _row, _col):
		if _col == self.LayerColumnSwitch:
			self.layersSwitchVis(_row, _col)



	def layersSwitchVis(self, _row, _col):
		cSelection = self.layerSelection()

		namesA = []
		newState = not self.lListLayers.item(_row, _col).data(self.LdataOn)


		if _row not in cSelection:
			self.lListLayers.selectRow(_row)
			cSelection = [_row]


		for cRow in cSelection:
			cItem = self.lListLayers.item(cRow, _col)
			if newState != cItem.data(self.LdataOn):
				self.layerSetItem(cItem, newState)
				namesA.append( cItem.data(self.LdataName) )


		self.sigCtrlLayersSet.emit(
			namesA,
			newState
		)



### DISPATCH ###

# -todo 59 (module-ui, ux, clean) +0: make updatable connections list
	def connList(self, _portsA):
		for port in _portsA:
			self.lDdPorts.insertItem(0,port)



	def dispatchRun(self):
		self.sigDispatch.emit( self.lDdPorts.currentText() )



	def dispatchLog(self, _txt):
		self.lLogDev.insertPlainText(_txt)
