#  todo 33 (module-ui, widgets) +0: zoom slider
#  todo 34 (module-ui, widgets) +0: transform reset


import os
import webbrowser

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

from .SvgViewport import *
from .MarkWidget import *



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

	sigSceneWipe = Signal()
	sigAddFile = Signal()
	sigSceneSave = Signal()
	sigSceneLoad = Signal()
	sigStoreG = Signal()
	sigDispatch = Signal(str)
	sigLayerSelect = Signal(list)
	sigLayerHover = Signal(str)
	sigCtrlLayersSet = Signal(list, bool)
	sigMarkAdd = Signal()
	sigMarkAssign = Signal(object, dict, bool)

	aboutHref = "https://github.com/NikolayRag/codeg"

	defaultWindowFit = 0.8
	defaultViewportFit = 0.8
	defaultViewportOffset = 0.66


## runtime ##

	allWidgetsMarks = {}



	def __init__(self, _uiFile, _styleFile=None):
		QObject.__init__(self)

		cMain = self.lMain = self.wMain = QUiLoader().load(_uiFile)


		if _styleFile:
			with open(_styleFile) as fQss:
				cMain.setStyleSheet(fQss.read())

		cMain.setWindowTitle('codeg');

		
		#widgets time
		self.wListObjects = cMain.findChild(QSplitter, "listObjects")


		self.wListGeoBlocks = cMain.findChild(QTableWidget, "listGeoBlocks")


		self.wListGeoItems = cMain.findChild(QTableWidget, "listGeoItems")

		self.wListGeoItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.wListGeoItems.itemSelectionChanged.connect(self.layerSelect)
		self.wListGeoItems.cellEntered.connect(self.layerHover)
		self.tmpFilterLayersLeave = BindFilter(QEvent.Type.Leave, self.layerHover)
		self.wListGeoItems.installEventFilter(self.tmpFilterLayersLeave)

		self.wListGeoItems.cellClicked.connect(self.layerClick)

		
		self.wMarkTools = cMain.findChild(QLayout, "wMarkTools")
		self.wMarks = cMain.findChild(QLayout, "wMarks")
		self.wBtnMarkAdd = cMain.findChild(QToolButton, "btnMarkAdd")


		holderViewport = cMain.findChild(QWidget, "wViewport")
		self.wViewport = SvgViewport(holderViewport)
		self.wViewport.setGrid('resource\\grid.svg')
		self.wViewport.lower()
		self.wViewport.show()

		self.tmpFilterViewResize = BindFilter(
			QEvent.Type.Resize,
			lambda event: self.wViewport.resize(event.size())
		)
		holderViewport.installEventFilter(self.tmpFilterViewResize)


		self.wBtnFit = cMain.findChild(QWidget, "btnFit")

		self.wBtnCaption = cMain.findChild(QWidget, "btnCaption")
		self.wBtnWipe = cMain.findChild(QWidget, "btnWipe")
		self.wBtnOpen = cMain.findChild(QWidget, "btnOpen")
		self.wBtnSave = cMain.findChild(QWidget, "btnSave")
		self.wBtnLoad = cMain.findChild(QWidget, "btnLoad")
		self.wBtnStore = cMain.findChild(QWidget, "btnStore")

		self.wFrameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.wFrameDispatcher.setVisible(False)
#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.wListPorts = cMain.findChild(QWidget, "listPorts")
		self.wBtnProccess = cMain.findChild(QWidget, "btnProccess")
		self.wFrameDev = cMain.findChild(QTextEdit, "frameDev")


		self.wBtnFit.clicked.connect(lambda: self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset))
		self.wBtnCaption.clicked.connect(self.about)
		self.wBtnWipe.clicked.connect(self.sigSceneWipe)
		self.wBtnOpen.clicked.connect(self.sigAddFile)
		self.wBtnSave.clicked.connect(self.sigSceneSave)
		self.wBtnLoad.clicked.connect(self.sigSceneLoad)
		self.wBtnStore.clicked.connect(self.sigStoreG)
		self.wBtnProccess.clicked.connect(self.dispatchRun)
		self.wBtnMarkAdd.clicked.connect(self.sigMarkAdd)
		

	def show(self):
		self.wMain.show()
		self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)



	def resize(self, _size, maximize=None):
		self.wMain.resize(
			QSize(*_size)
			if _size else
			QApplication.primaryScreen().size() * self.defaultWindowFit
		)

		if maximize:
			self.wMain.showMaximized()



	def about(self):
		webbrowser.open(self.aboutHref)



	def slotNewScene(self, _scene):
		self.wBtnStore.setEnabled(True)
		self.wBtnProccess.setEnabled(True)
		self.wListGeoItems.setRowCount(0)


		while markTool := self.wMarkTools.takeAt(0):
			markTool.widget().setParent(None)


		while wMark := self.wMarks.takeAt(0):
			wMark.widget().setParent(None)



		self.allWidgetsMarks = {}


		self.wViewport.canvasReset()
		self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)
		self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)


#		Marks



#  todo 3 (feature, file) +0: allow picking from Recent files list
	def reactAddFile(self, _meta, _xml):
		self.wViewport.canvasAdd(_xml)
		self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)
#  todo 157 (fix, canvas) +0: review SvgViewport fit routine
		self.wViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)


		cList = self.wListGeoItems

		for cName in _meta:
			self.layerAddItem(cList, _meta, cName)

		#blank
		self.layerAddItem(cList)



#  todo 20 (module-ui, error) +0: handle errors, maybe status string
	def reactStoreG(self):
		None



	def canvasUpdate(self, _xml):
		self.wViewport.canvasUpdate(_xml)



######### Geoitems #########
# -todo 150 (ux, widgets) +0: Make GeoWidget

# =todo 144 (module-ui, widgets) +0: Use Geoitems directly in UI
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
			visible = ('visible' not in _meta[_name]) or _meta[_name]['visible']
			self.layerSetItem(itemOn, visible)
			_list.setItem(cRow, self.LayerColumnSwitch, itemOn)

		else:
			for i in range(_list.columnCount()):
				cItem = QTableWidgetItem()
				cItem.setFlags(Qt.NoItemFlags)
				_list.setItem(cRow, i, cItem)



	def layerSelection(self):
		out = {}

		for cRange in self.wListGeoItems.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cName = self.wListGeoItems.item(cRow, self.LayerColumnName)
				out[cRow] = cName.data(self.LdataName)

		return out



	def layerSelect(self):
		cSel = self.layerSelection().values()
		self.sigLayerSelect.emit(list(cSel))



	def marksSelect(self, _marks):
		for cMark in self.allWidgetsMarks:
			self.allWidgetsMarks[cMark].setTrigger(False, emit=False)


		for cMark in _marks:
			if cMark in self.allWidgetsMarks:
				self.allWidgetsMarks[cMark].setTrigger(_marks[cMark], tri=not _marks[cMark], emit=False)



	def layerHover(self, _row=-1, _col=-1, event=None):
		hoverName = None
		if _row >= 0:
			hoverName = self.wListGeoItems.item(_row, self.LayerColumnName).data(self.LdataName)


		self.sigLayerHover.emit(hoverName)



	def layerClick(self, _row, _col):
		if _row == self.wListGeoItems.rowCount()-1:
			self.wListGeoItems.clearSelection()

			return
			

		if _col == self.LayerColumnSwitch:
			self.layersSwitchVis(_row, _col)



	def layersSwitchVis(self, _row, _col):
		cSelection = list(self.layerSelection().keys())
		namesA = []
		newState = not self.wListGeoItems.item(_row, _col).data(self.LdataOn)


		if _row not in cSelection:
			self.wListGeoItems.selectRow(_row)
			cSelection = [_row]


# =todo 114 (module-ui, fix) +0: change vis for select-all case
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection
		for cRow in cSelection:
			cItem = self.wListGeoItems.item(cRow, _col)
			if newState == cItem.data(self.LdataOn):
				continue

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
			self.wListPorts.insertItem(0,port)



	def dispatchRun(self):
		self.sigDispatch.emit( self.wListPorts.currentText() )



	def dispatchLog(self, _txt):
		self.wFrameDev.insertPlainText(_txt)



### MARKS ###

#  todo 152 (module-ui, mark) +0: make select by mark
#  todo 153 (module-ui, mark) +0: manage mark fields list
# -todo 145 (module-ui, widgets) +0: make Marks arrangable with priority change (DragList)
	def wMarkAdd(self, _mark, _open, fieldColor=''):
		if _mark in self.allWidgetsMarks:
			print('MarkWidget already exists')
			return


		btnMark = MarkWidget(self.wMarkTools, _mark, fieldWColor=fieldColor)
		self.allWidgetsMarks[_mark] = btnMark


		self.wMarks.addWidget(btnMark)

		btnMark.sigChanged.connect(lambda m,n,v:print(f"Changed: {m} '{n}' to {v}"))
		btnMark.sigTrigger.connect(lambda m,s:self.sigMarkAssign.emit(m, self.layerSelection(), s))
	 
		if _open:
			btnMark.toolPop()



# -todo 141 (module-ui, mark) +0: update Geoitem widgets
	def wMarkAssign(self, _mark, _geoList, _state):
		None
