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

from .BindFilter import *



class AppWindow(QObject):
	sigPreexit = Signal(object)

	sigGeoSelect = Signal(object, bool)
	sigGeoHover = Signal(object, bool)
	sigGeoDataSet = Signal(object, list)
	sigMarkAdd = Signal()
	sigGeoActivate = Signal(object, bool)

	sigSceneReset = Signal()
	sigSceneSave = Signal()
	sigSceneLoad = Signal()
	sigAddFile = Signal()

	sigDispatch = Signal(str)
	sigStoreG = Signal()


	aboutHref = "https://github.com/NikolayRag/codeg"

	defGrid = 'resource\\grid.svg' #1-unit size
	defUi = './Ui/AppWindow.ui'

	defaultWindowFit = 0.8
	defaultViewportFit = 0.8
	defaultViewportOffset = 0.66


## runtime ##

	gridDescription = None
#  todo 212 (module-ui, clean, widget) +0: MarkWidget collection class
	widgetGeo = None
	allWidgetsMarks = {}



	def __init__(self, _styleFile=None):
		QObject.__init__(self)

		cMain = self.lMain = self.wMain = QUiLoader().load(self.defUi)
		self.tmpFilterPreexit = BindFilter({
			QEvent.Close: lambda event: self.sigPreexit.emit(event) or True })
		cMain.installEventFilter(self.tmpFilterPreexit)


		if _styleFile:
			with open(_styleFile) as fQss:
				cMain.setStyleSheet(fQss.read())

		cMain.setWindowTitle('codeg');

		
		#widgets time
#  todo 215 (module-ui) +0: cleanup GeoWidget ui collection
		wFrameGeoBlocks = cMain.findChild(QLayout, "frameGeoBlocks")
		wFrameGeoWid = cMain.findChild(QLayout, "frameGeo")
		self.widgetGeo = GeoWidget(wFrameGeoBlocks, wFrameGeoWid)

		listObjects = cMain.findChild(QSplitter, "listObjects")
		listObjects.setStretchFactor(1, 1)

		self.widgetGeo.sigItemSelect.connect(lambda item, state: self.sigGeoSelect.emit(item, state))
		self.widgetGeo.sigItemHover.connect(lambda item, state: self.sigGeoHover.emit(item, state))
		self.widgetGeo.sigItemDataSet.connect(lambda item, names: self.sigGeoDataSet.emit(item, names))
		self.widgetGeo.sigTouchRun.connect(self.suspend)
		self.widgetGeo.sigTouched.connect(self.geoWidgetTouched)
		self.widgetGeo.sigSelected.connect(self.geoWidgetSelected)
		self.widgetGeo.sigActivate.connect(lambda block, state: self.sigGeoActivate.emit(block, state))


		self.wFrameMark = cMain.findChild(QLayout, "frameMark")
		self.wMarks = cMain.findChild(QLayout, "wMarks")
		self.wBtnMarkAdd = cMain.findChild(QToolButton, "btnMarkAdd")


		holderViewport = cMain.findChild(QWidget, "wViewport")
		self.wSvgViewport = SvgViewport(holderViewport)
		self.wSvgViewport.lower() 


		self.tmpFilterViewResize = BindFilter({
			QEvent.Type.Resize: lambda event: self.wSvgViewport.resize(event.size()) })
		holderViewport.installEventFilter(self.tmpFilterViewResize)

		self.wSvgViewport.sigInteract.connect(self.viewportInteract)


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


		self.wBtnFit.clicked.connect(self.viewportFit)
		self.wBtnCaption.clicked.connect(self.about)
		self.wBtnWipe.clicked.connect(self.sigSceneReset)
		self.wBtnOpen.clicked.connect(self.sigAddFile)
		self.wBtnSave.clicked.connect(self.sigSceneSave)
		self.wBtnLoad.clicked.connect(self.sigSceneLoad)
		self.wBtnStore.clicked.connect(self.sigStoreG)
		self.wBtnProccess.clicked.connect(self.dispatchRun)
		self.wBtnMarkAdd.clicked.connect(self.sigMarkAdd)
		

	def show(self):
		self.wMain.show()
#  todo 192 (module-ui, fix) +0: wrong fit at start
		self.viewportFit()



	def resize(self, _size, maximize=None):
		self.wMain.resize(
			QSize(*_size)
			if _size else
			QApplication.primaryScreen().size() * self.defaultWindowFit
		)

		if maximize:
			self.wMain.showMaximized()



	def suspend(self, _state):
		self.lMain.setUpdatesEnabled(not _state)



	def about(self):
		webbrowser.open(self.aboutHref)



### VIEWPORT ###


	def viewportFit(self):
		self.wSvgViewport.canvasFit(self.defaultViewportFit, self.defaultViewportOffset)



	def viewportInteract(self, _step, _point, _origin, _mod, _spot=True):
		if _mod == Qt.NoModifier:
			for cGeo in self.widgetGeo.getBlocks().keys():
				xmm = sorted((_origin.x(),_point.x()))
				ymm = sorted((_origin.y(),_point.y()))

				cGeo.boxed(xmm, ymm, _origin.x()>_point.x())


			if _step == SvgViewport.intEnd and _spot:
				self.widgetGeo.selectGeo(None)
				MarkWidget.toolUnpop()

				return


		if _mod!=Qt.ShiftModifier:
			return


		cOffset = _point -_origin

		for cGeo, cDscr in self.widgetGeo.getBlocks().items():
			gOffset = cGeo.xformSet()
			gOffset = (gOffset[0][2], gOffset[1][2])
			_offset = (
				gOffset[0] +cOffset.x(),
				gOffset[1] +cOffset.y()
			)

			if _step == SvgViewport.intLive:
				cDscr.place(_offset)

			if _step == SvgViewport.intEnd:
				cGeo.xformSet(offset=_offset)

			if _step == SvgViewport.intCancel:
				cDscr.place(gOffset)



### GEO ###
#  todo 213 (ux, viewport) +0: place support viewport layer for block
	def geoAddWidget(self, _geo):
		gOffset = _geo.xformSet()
		gOffset = (gOffset[0][2], gOffset[1][2])
		cXml = _geo.xmlString()
		cDscr = self.wSvgViewport.canvasAdd(cXml, gOffset)

		self.widgetGeo.blockAdd(_geo, cDscr)



	def geoWidgetTouched(self, _block, _descr):
		_descr.setXml( _block.xmlString() )



	def geoWidgetSelected(self, _selection):
		marksUsed = {}
		
		for cObj in _selection:
			for cMark in cObj.markList():
				marksUsed[cMark] = True #assigned

		for cMark in marksUsed:
			for cObj in _selection:
				if not cObj.markAssigned(cMark):
					marksUsed[cMark] = False #also unassigned


		for cMark in self.allWidgetsMarks:
			self.allWidgetsMarks[cMark].setTrigger(False)


		for cMark, cIn in marksUsed.items():
			if cMark in self.allWidgetsMarks:
				self.allWidgetsMarks[cMark].setTrigger(cIn, tri=not cIn)



### MARKS ###


# =todo 152 (module-ui, mark) +0: make select by mark
#  todo 153 (module-ui, mark) +0: manage mark fields list
#  todo 145 (module-ui, widgets) +0: make Marks arrangable with priority change (DragList)
	def markAddWidget(self, _mark, _open=False, colorName=''):
		if _mark in self.allWidgetsMarks:
			print('MarkWidget already exists')
			return


		btnMark = MarkWidget(self.wFrameMark, _mark, colorFieldName=colorName)
		self.allWidgetsMarks[_mark] = btnMark


		self.wMarks.addWidget(btnMark)

		btnMark.sigChanged.connect(self.markChanged)
		btnMark.sigTrigger.connect(self.markAssign)

		if _open:
			btnMark.toolPop()



# -todo 141 (module-ui, mark) +0: update Geoitem widgets on Mark assign
	def markChanged(self, _mark, _name, _val):
		None



	def markAssign(self, _mark, _state):
		cGeoList = self.widgetGeo.currentSelection()

		for cGeo in cGeoList:
			cGeo.markSet(_mark, _state)

			cGeo.marksSolve(filterStep='DIRECT')



### DISPATCH ###

# -todo 59 (module-ui, ux, clean) +0: make updatable connections list
	def connList(self, _portsA):
		for port in _portsA:
			self.wListPorts.insertItem(0,port)



	def dispatchRun(self):
		self.sigDispatch.emit( self.wListPorts.currentText() )



	def dispatchLog(self, _txt):
		self.wFrameDev.insertPlainText(_txt)



### HIPE ###


	def slotNewScene(self, _scene):
		self.wBtnStore.setEnabled(True)
		self.wBtnProccess.setEnabled(True)
		self.widgetGeo.clean()


		while markTool := self.wFrameMark.takeAt(0):
			markTool.widget().setParent(None)


		while wMark := self.wMarks.takeAt(0):
			wMark.widget().setParent(None)



		self.allWidgetsMarks = {}


# =todo 89 (ux, module-ui, fix) +0: place grid correctly
		self.wSvgViewport.canvasReset()
		self.gridDescription = self.wSvgViewport.canvasAdd(self.defGrid)



	def gridSize(self, _size):
		self.gridDescription.size(_size)
		self.gridDescription.place((0,-_size[1]))



#  todo 20 (module-ui, error) +0: handle errors, maybe status string
	def reactStoreG(self):
		None
