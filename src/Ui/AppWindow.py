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
from .GeoWidget import *



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
			return True


		return False



class AppWindow(QObject):
	LayerColumnName = 0
	LayerColumnSwitch = 1

	LdataName = Qt.UserRole +0
	LdataOn = Qt.UserRole +2

	sigPreexit = Signal(object)
	sigSceneWipe = Signal()
	sigAddFile = Signal()
	sigSceneSave = Signal()
	sigSceneLoad = Signal()
	sigStoreG = Signal()
	sigDispatch = Signal(str)
	sigGeoSelect = Signal(object, bool)
	sigGeoHover = Signal(object, bool)
	sigGeoDataSet = Signal(object, list)
	sigGeoChanged = Signal()
	sigMarkAdd = Signal()
	sigMarkAssign = Signal(object, dict, bool)

	aboutHref = "https://github.com/NikolayRag/codeg"

	defUi = './Ui/AppWindow.ui'

	defaultWindowFit = 0.8
	defaultViewportFit = 0.8
	defaultViewportOffset = 0.66


## runtime ##

	allWidgetsMarks = {}



	def __init__(self, _styleFile=None):
		QObject.__init__(self)

		cMain = self.lMain = self.wMain = QUiLoader().load(self.defUi)
		self.tmpFilterPreexit = BindFilter(
			QEvent.Close,
			lambda event: self.sigPreexit.emit(event)
		)
		cMain.installEventFilter(self.tmpFilterPreexit)


		if _styleFile:
			with open(_styleFile) as fQss:
				cMain.setStyleSheet(fQss.read())

		cMain.setWindowTitle('codeg');

		
		#widgets time
		self.wListObjects = cMain.findChild(QSplitter, "listObjects")


		self.wListGeoBlocks = cMain.findChild(QTableWidget, "listGeoBlocks")


		self.wFrameGeo = cMain.findChild(QLayout, "frameGeo")
		self.wGeoWidget = GeoWidget()
		self.wFrameGeo.addWidget(self.wGeoWidget)

		self.wGeoWidget.sigItemSelect.connect(lambda item, state: self.sigGeoSelect.emit(item, state))
		self.wGeoWidget.sigItemHover.connect(lambda item, state: self.sigGeoHover.emit(item, state))
		self.wGeoWidget.sigItemDataSet.connect(lambda item, names: self.sigGeoDataSet.emit(item, names))
		self.wGeoWidget.sigChanged.connect(self.geoTouched)


		self.wFrameMark = cMain.findChild(QLayout, "frameMark")
		self.wMarks = cMain.findChild(QLayout, "wMarks")
		self.wBtnMarkAdd = cMain.findChild(QToolButton, "btnMarkAdd")


		holderViewport = cMain.findChild(QWidget, "wViewport")
		self.wSvgViewport = SvgViewport(holderViewport)
		self.wSvgViewport.setGrid('resource\\grid.svg')
		self.wSvgViewport.lower()
		self.wSvgViewport.show()

		self.tmpFilterViewResize = BindFilter(
			QEvent.Type.Resize,
			lambda event: self.wSvgViewport.resize(event.size())
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


		self.wBtnFit.clicked.connect(lambda: self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset))
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
#  todo 192 (module-ui, fix) +0: wrong fit at start
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)



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
		self.wGeoWidget.clean()


		while markTool := self.wFrameMark.takeAt(0):
			markTool.widget().setParent(None)


		while wMark := self.wMarks.takeAt(0):
			wMark.widget().setParent(None)



		self.allWidgetsMarks = {}


		self.wSvgViewport.canvasReset()
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)



#  todo 3 (feature, file) +0: allow picking from Recent files list
	def viewportSet(self, _xml):
		self.wSvgViewport.canvasAdd(_xml)
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)
#  todo 157 (fix, canvas) +0: review SvgViewport fit routine
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)



#  todo 20 (module-ui, error) +0: handle errors, maybe status string
	def reactStoreG(self):
		None



	def viewportUpdate(self, _xml):
		self.wSvgViewport.canvasUpdate(_xml)



######### Geoitems #########

	def geoAddSlot(self, _geo):
		self.wGeoWidget.replace(_geo)



	def geoTouched(self, _selected):
		self.sigGeoChanged.emit()

		if not _selected:
			return


		marksUsed = {}
		
		cSelected = self.wGeoWidget.getItems(selected=True)

		for cObj in cSelected:
			for cMark in cObj.marks:
				marksUsed[cMark] = True

		for cMark in marksUsed:
			for cObj in cSelected:
				if cMark not in cObj.marks:
					marksUsed[cMark] = False


		for cMark in self.allWidgetsMarks:
			self.allWidgetsMarks[cMark].setTrigger(False, emit=False)


		for cMark, cIn in marksUsed.items():
			if cMark in self.allWidgetsMarks:
				self.allWidgetsMarks[cMark].setTrigger(cIn, tri=not cIn, emit=False)



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


		btnMark = MarkWidget(self.wFrameMark, _mark, fieldWColor=fieldColor)
		self.allWidgetsMarks[_mark] = btnMark


		self.wMarks.addWidget(btnMark)

		btnMark.sigChanged.connect(lambda m,n,v:print(f"Changed: {m} '{n}' to {v}"))
		btnMark.sigTrigger.connect(lambda m,s:self.sigMarkAssign.emit(m, self.wGeoWidget.getItems(selected=True), s))
	 
		if _open:
			btnMark.toolPop()



# -todo 141 (module-ui, mark) +0: update Geoitem widgets on Mark assign
