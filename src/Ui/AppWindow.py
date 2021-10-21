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

	defaultWindowFit = defaultViewportFit = 0.8


## runtime ##

	allWidgetsMarks = {}



	def __init__(self, _uiFile, _styleFile=None):
		QObject.__init__(self)

		cMain = self.lMain = QUiLoader().load(_uiFile)


		if _styleFile:
			with open(_styleFile) as fQss:
				cMain.setStyleSheet(fQss.read())

		cMain.setWindowTitle('codeg');

		
		#widgets time
		self.lGeoView = cMain.findChild(QSplitter, "wGeoView")


		self.lListLayers = cMain.findChild(QTableWidget, "listLayers")

		self.lListLayers.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.lListLayers.itemSelectionChanged.connect(self.layerSelect)
		self.lListLayers.cellEntered.connect(self.layerHover)
		self.tmpFilterLayersLeave = BindFilter(QEvent.Type.Leave, self.layerHover)
		self.lListLayers.installEventFilter(self.tmpFilterLayersLeave)

		self.lListLayers.cellClicked.connect(self.layerClick)

		
		self.layMarkHolder = cMain.findChild(QLayout, "layMarkHolder")
		self.scrollMarksLayout = cMain.findChild(QLayout, "scrollMarksLayout")
		self.btnMarkAdd = cMain.findChild(QToolButton, "btnMarkAdd")


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
		self.lBtnWipe = cMain.findChild(QWidget, "btnWipe")
		self.lBtnOpen = cMain.findChild(QWidget, "btnOpen")
		self.lBtnSave = cMain.findChild(QWidget, "btnSave")
		self.lBtnLoad = cMain.findChild(QWidget, "btnLoad")
		self.lBtnStore = cMain.findChild(QWidget, "btnStore")

		self.lFrameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.lFrameDispatcher.setVisible(False)
#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.lDdPorts = cMain.findChild(QWidget, "ddPorts")
		self.lBtnProccess = cMain.findChild(QWidget, "btnProccess")
		self.lLogDev = cMain.findChild(QTextEdit, "logDev")


		self.lBtnFit.clicked.connect(lambda: self.lViewport.canvasFit(self.defaultViewportFit))
		self.lBtnCaption.clicked.connect(self.about)
		self.lBtnWipe.clicked.connect(self.sigSceneWipe)
		self.lBtnOpen.clicked.connect(self.sigAddFile)
		self.lBtnSave.clicked.connect(self.sigSceneSave)
		self.lBtnLoad.clicked.connect(self.sigSceneLoad)
		self.lBtnStore.clicked.connect(self.sigStoreG)
		self.lBtnProccess.clicked.connect(self.dispatchRun)
		self.btnMarkAdd.clicked.connect(self.sigMarkAdd)
		

	def show(self):
		self.lMain.show()
		self.lViewport.canvasFit(self.defaultViewportFit)



	def resize(self, _size, maximize=None):
		self.lMain.resize(
			QSize(*_size)
			if _size else
			QApplication.primaryScreen().size() * self.defaultWindowFit
		)

		if maximize:
			self.lMain.showMaximized()



	def about(self):
		webbrowser.open(self.aboutHref)



	def slotNewScene(self, _scene):
		self.lBtnStore.setEnabled(True)
		self.lBtnProccess.setEnabled(True)
		self.lListLayers.setRowCount(0)


		while markTool := self.layMarkHolder.takeAt(0):
			markTool.widget().setParent(None)


		while wMark := self.scrollMarksLayout.takeAt(0):
			wMark.widget().setParent(None)



		self.allWidgetsMarks = {}


		self.lViewport.canvasReset()
		self.lViewport.canvasFit(self.defaultViewportFit)
		self.lViewport.canvasFit(self.defaultViewportFit)


#		Marks



#  todo 3 (feature, file) +0: allow picking from Recent files list
	def reactAddFile(self, _meta, _xml):
		self.lViewport.canvasAdd(_xml)
		self.lViewport.canvasFit(self.defaultViewportFit)
#  todo 157 (fix, canvas) +0: review SvgViewport fit routine
		self.lViewport.canvasFit(self.defaultViewportFit)


		cList = self.lListLayers

		for cName in _meta:
			self.layerAddItem(cList, _meta, cName)

		#blank
		self.layerAddItem(cList)



#  todo 20 (module-ui, error) +0: handle errors, maybe status string
	def reactStoreG(self):
		None



	def canvasUpdate(self, _xml):
		self.lViewport.canvasUpdate(_xml)



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

		for cRange in self.lListLayers.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cName = self.lListLayers.item(cRow, self.LayerColumnName)
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
			hoverName = self.lListLayers.item(_row, self.LayerColumnName).data(self.LdataName)


		self.sigLayerHover.emit(hoverName)



	def layerClick(self, _row, _col):
		if _row == self.lListLayers.rowCount()-1:
			self.lListLayers.clearSelection()

			return
			

		if _col == self.LayerColumnSwitch:
			self.layersSwitchVis(_row, _col)



	def layersSwitchVis(self, _row, _col):
		cSelection = list(self.layerSelection().keys())
		namesA = []
		newState = not self.lListLayers.item(_row, _col).data(self.LdataOn)


		if _row not in cSelection:
			self.lListLayers.selectRow(_row)
			cSelection = [_row]


# =todo 114 (module-ui, fix) +0: change vis for select-all case
# -todo 147 (module-ui, fix) +0: use blank layer space to from-to hover mouse selection
		for cRow in cSelection:
			cItem = self.lListLayers.item(cRow, _col)
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
			self.lDdPorts.insertItem(0,port)



	def dispatchRun(self):
		self.sigDispatch.emit( self.lDdPorts.currentText() )



	def dispatchLog(self, _txt):
		self.lLogDev.insertPlainText(_txt)



### MARKS ###

#  todo 152 (module-ui, mark) +0: make select by mark
#  todo 153 (module-ui, mark) +0: manage mark fields list
# -todo 145 (module-ui, widgets) +0: make Marks arrangable with priority change (DragList)
	def wMarkAdd(self, _mark, _open, fieldColor=''):
		if _mark in self.allWidgetsMarks:
			print('MarkWidget already exists')
			return


		btnMark = MarkWidget(self.layMarkHolder, _mark, fieldWColor=fieldColor)
		self.allWidgetsMarks[_mark] = btnMark


		self.scrollMarksLayout.addWidget(btnMark)

		btnMark.sigChanged.connect(lambda m,n,v:print(f"Changed: {m} '{n}' to {v}"))
		btnMark.sigTrigger.connect(lambda m,s:self.sigMarkAssign.emit(m, self.layerSelection(), s))
	 
		if _open:
			btnMark.toolPop()



# -todo 141 (module-ui, mark) +0: update Geoitem widgets
	def wMarkAssign(self, _mark, _geoList, _state):
		None
