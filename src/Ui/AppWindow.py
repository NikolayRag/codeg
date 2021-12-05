#  todo 33 (module-ui, widgets) +0: zoom slider
#  todo 34 (module-ui, widgets) +0: transform reset


import os
import webbrowser

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

from Args import *

from .PrefsWidget import *
from .SvgViewport import *
from .MarkWidget import *
from .GeoWidget import *

from .BindFilter import *
from .Tracer import *



class AppWindow(QObject):
	sigPrefScheme = Signal()
	sigPreexit = Signal(object)

	sigGeoSelect = Signal(object, bool)
	sigGeoHover = Signal(object, bool)
	sigGeoDataSet = Signal(object, list)
	sigMarkAdd = Signal()
	sigGeoActivate = Signal(object, bool)

	sigSceneReset = Signal()
	sigSceneSave = Signal(object)
	sigSceneLoad = Signal(object)
	sigAddFile = Signal(object)
	sigPaste = Signal()
	sigDrop = Signal(list)

	sigDevScan = Signal()
	sigDevChange = Signal(str, object)
	sigDispatchFire = Signal()
	sigDispatchShot = Signal(object)


	aboutHref = "https://github.com/NikolayRag/codeg"

	defSelection = 'resource\\select.svg'
	defGrid = 'resource\\grid.svg' #1-unit size
	defUi = './Ui/AppWindow.ui'


## runtime ##

	selectionDescription = None
	selectionCache = []

	gridDescription = None

	tracer = None


#  todo 212 (module-ui, clean, widget) +0: MarkWidget collection class
	widgetGeo = None
	allWidgetsMarks = {}

	rtSize = []
	rtPos = []


	def __init__(self):
		QObject.__init__(self)

		self.rtSize = [None, None]
		self.rtPos = [None, None]


		cMain = self.wMain = QUiLoader().load(self.defUi)
		cMain.setWindowTitle('codeg');

#  todo 244 (feature) +0: add drop scene, svg files and tag text
		self.tmpFilterMain = BindFilter({
			QEvent.Close: lambda event: self.sigPreexit.emit(event) or True,
			QEvent.Move: self.moved,
			QEvent.Resize: self.resized,
			QEvent.WindowStateChange: self.maximized,
			QEvent.DragEnter: lambda e: e.acceptProposedAction(),
			QEvent.Drop: lambda e: e.mimeData().hasUrls() and self.sigDrop.emit(e.mimeData().urls()),
		 })
		cMain.installEventFilter(self.tmpFilterMain)

		
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
		self.wSvgViewport = SvgViewport(holderViewport, Args.Viewport)
		self.wSvgViewport.lower() 


		self.tmpFilterViewResize = BindFilter({
			QEvent.Type.Resize: lambda event: self.wSvgViewport.resize(event.size()) })
		holderViewport.installEventFilter(self.tmpFilterViewResize)

		self.wSvgViewport.sigInteract.connect(self.viewportInteract)


		self.wBtnFit = cMain.findChild(QWidget, "btnFit")
		self.wBtnTraceView = cMain.findChild(QWidget, "btnTraceView")
		self.wBtnTraceView.setChecked(Args.Viewport.visTracer)

		self.wBtnCaption = cMain.findChild(QWidget, "btnCaption")
		self.wBtnWipe = cMain.findChild(QWidget, "btnWipe")
		self.wBtnOpen = cMain.findChild(QWidget, "btnOpen")
		self.wBtnSave = cMain.findChild(QWidget, "btnSave")
		self.wBtnLoad = cMain.findChild(QWidget, "btnLoad")
		self.wBtnDispShot = cMain.findChild(QWidget, "btnDispShot")
		self.wBtnPaste = cMain.findChild(QWidget, "btnPaste")
		self.wBtnPrefs = cMain.findChild(QWidget, "btnPrefs")

		self.wBtnDispatcher = cMain.findChild(QWidget, "btnDispatcher")
		self.wFrameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.wBtnDispatcher.setChecked(Args.Dispatch.visDispatch)

#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.wBtnRescan = cMain.findChild(QWidget, "btnRescan")
		self.wListDevs = cMain.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = cMain.findChild(QWidget, "btnDispFire")


		self.wFrameDev = cMain.findChild(QWidget, "frameDev")
		self.wLabStats = cMain.findChild(QWidget, "labStats")
		self.wTraceProg = cMain.findChild(QWidget, "traceProg")

		fm = QFontMetrics(self.wLabStats.document().defaultFont())
		self.wLabStats.setMaximumHeight(fm.height()*3)


		self.wBtnFit.clicked.connect(self.viewportFit)
		self.wBtnDispatcher.toggled.connect(self.dispatchToggle)
		self.wBtnTraceView.toggled.connect(self.traceToggle)
		self.wBtnCaption.clicked.connect(self.about)
		self.wBtnWipe.clicked.connect(self.sigSceneReset)
		self.wBtnOpen.clicked.connect(lambda: self.sigAddFile.emit(self.wMain))
		self.wBtnPaste.clicked.connect(self.sigPaste)
		self.wBtnSave.clicked.connect(lambda: self.sigSceneSave.emit(self.wMain))
		self.wBtnLoad.clicked.connect(lambda: self.sigSceneLoad.emit(self.wMain))
		self.wBtnRescan.clicked.connect(self.sigDevScan)
		self.wBtnDispShot.clicked.connect(lambda: self.sigDispatchShot.emit(self.wMain))
		self.wBtnDispFire.clicked.connect(self.sigDispatchFire)
		self.wBtnMarkAdd.clicked.connect(self.sigMarkAdd)
		self.wListDevs.currentIndexChanged.connect(lambda i: self.sigDevChange.emit(self.wListDevs.currentText(), self.wListDevs.currentData()))
		self.wBtnPrefs.clicked.connect(self.prefsList)
		
#  todo 280 (ui, feature) +0: makeTracer Ui-wide
#  todo 281 (ui, clean) +0: make Tracer OSD unweird
		self.tracer = Tracer(
			lambda z:self.wSvgViewport.canvasAdd(z=100+z),
			[self.wFrameDev, self.wLabStats, self.wTraceProg]
		)

		self.dispatchToggle(Args.Dispatch.visDispatch)
		self.traceToggle(Args.Viewport.visTracer)



	def setStyle(self, _styleFn):
		with open(_styleFn) as fQss:
			self.wMain.setStyleSheet(fQss.read())



	def show(self):
		self.wMain.show()

		self.viewportFit() #initial



	def windowGeometry(self):
		return [self.rtSize[1], self.rtPos[1], self.wMain.isMaximized()]



	#specific logic relying on events order
	def moved(self, _e):
		if self.rtPos[1]:
			self.rtPos[0] = self.rtPos[1]
			self.rtPos[1] = self.wMain.pos()
		else:
			self.rtPos[1] = self.rtPos[0]


	def resized(self, _e):
		if self.rtSize[1]:
			self.rtSize[0] = self.rtSize[1]
			self.rtSize[1] = self.wMain.size()
		else:
			self.rtSize[1] = self.rtSize[0]


	def maximized(self, _e):
		if self.wMain.isMaximized():
			self.rtSize[1] = self.rtSize[0]
			self.rtPos[1] = self.rtPos[0]



	def windowGeometrySet(self, _size, _pos, maximize=None):
		self.wMain.resize( _size )

		self.wMain.move( _pos )

		if maximize:
			self.wMain.showMaximized()

		#marker values to pass to following events
		self.rtSize = [_size,None]
		self.rtPos = [_pos,None]



	def suspend(self, _state):
		self.wMain.setUpdatesEnabled(not _state)



	def about(self):
		webbrowser.open(self.aboutHref)



### VIEWPORT ###


	def viewportFit(self, _box=None, _fit=None, _offset=None):
		countGrid = bool(self.widgetGeo.getBlocks())
		self.gridDescription.ghost(countGrid)

		self.wSvgViewport.canvasFit(_box, _fit, _offset)



	def viewportMouseMove(self, _offset, _step):
		for cGeo, cDscr in self.widgetGeo.getBlocks().items():
			gOffset = cGeo.xformSet()
			gOffset = (gOffset[0][2], gOffset[1][2])
			_offset = (
				gOffset[0] +_offset.x(),
				gOffset[1] +_offset.y()
			)

			if _step == SvgViewport.intLive:
				cDscr.place(_offset)

			if _step == SvgViewport.intEnd:
				cGeo.xformSet(offset=_offset)

			if _step == SvgViewport.intCancel:
				cDscr.place(gOffset)



	def viewportMouseSelect(self, _point, _origin, _step, _spot):
		self.selectionDescription.fit(_point,_origin)

		if _step == SvgViewport.intStart:
			self.selectionCache = self.widgetGeo.currentSelection()

			self.selectionDescription.show(True)


		if (_step == SvgViewport.intLive and not _spot) or _step == SvgViewport.intStart:
			for cGeo, cDescr in self.widgetGeo.getBlocks().items():
				xmm = sorted((_origin.x(),_point.x()))
				ymm = sorted((_origin.y(),_point.y()))

				inthebox = cGeo.boxed(xmm, ymm, _origin.x()>_point.x())
				self.widgetGeo.selectGeo(inthebox)


		if _step == SvgViewport.intLive or _step == SvgViewport.intStart:
			return


		self.selectionDescription.show(False)

		if _step == SvgViewport.intCancel:
			self.widgetGeo.selectGeo(self.selectionCache)

			return



	def viewportInteract(self, _step, _point, _origin, _mod, _spot=True):
		if _mod == Qt.NoModifier:
			self.viewportMouseSelect(_point, _origin, _step, _spot)

		if _mod==Qt.ShiftModifier:
			self.viewportMouseMove(_point -_origin, _step)



### GEO ###
#  todo 213 (ux, viewport) +0: place support viewport layer for block
	def geoAddWidget(self, _geo):
		gX = _geo.xformSet()
		gOffset = (gX[0][2], gX[1][2])
		gScale = (gX[0][0], gX[1][1])
		cXml = _geo.xmlString()
		cDscr = self.wSvgViewport.canvasAdd(cXml, gOffset, gScale)

		self.widgetGeo.blockAdd(_geo, cDscr)

		return cDscr



	def geoWidgetTouched(self, _block=None, _descr=None):
		if _block:
			_descr.setXml( _block.xmlString() )
			return


		for geoBlock, geoDescr in self.widgetGeo.getBlocks(True).items():
			geoDescr.setXml( geoBlock.xmlString() )



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


	def dispatchToggle(self, _state):
		self.wFrameDev.setVisible(_state)
		self.wLabStats.setVisible(_state)
		self.wTraceProg.setVisible(_state)

		self.wSvgViewport.canvasUpdate(False)
		self.tracer.show(spots=_state)
		self.wSvgViewport.canvasUpdate(True)

		self.wFrameDispatcher.setVisible(_state)
		self.wBtnTraceView.setVisible(_state)

		Args.Dispatch.visDispatch = _state



	def dispatchFill(self, _devices, _default, add=False):
		oldList = {self.wListDevs.itemText(i):self.wListDevs.itemData(i) for i in range(self.wListDevs.count())}

		if add:
			_devices = set([_devices]) | set(oldList.keys())


		self.wListDevs.blockSignals(True)
		self.wListDevs.clear()
		self.wListDevs.blockSignals(False)


		if _default not in _devices:
			self.wListDevs.addItem(_default, False)
			self.wListDevs.setCurrentIndex(self.wListDevs.count()-1)


		for devName in _devices:
			self.wListDevs.addItem(devName, True)

			if devName == _default:
				self.wListDevs.setCurrentIndex(self.wListDevs.count()-1)



	def traceQueue(self, _session):
		print(_session)


	def traceStart(self, _session):
		self.tracer.reset(_session)


	def traceFeed(self, _res, _echo):
		self.tracer.feed(_res, _echo)


	def traceEnd(self, _session, _res):
		self.tracer.final(_res)


### SCENE ###


	def slotNewScene(self, _scene):
		self.widgetGeo.clean()


		while markTool := self.wFrameMark.takeAt(0):
			markTool.widget().setParent(None)


		while wMark := self.wMarks.takeAt(0):
			wMark.widget().setParent(None)



		self.allWidgetsMarks = {}


		self.wSvgViewport.canvasReset()
		self.gridDescription = self.wSvgViewport.canvasAdd(self.defGrid)

		self.selectionDescription = self.wSvgViewport.canvasAdd(self.defSelection, z=99)
		self.selectionDescription.show(False)

		self.tracer.reset()



	def gridSize(self, _size):
		self.gridDescription.size(_size)
		self.gridDescription.place((0,-_size[1]))



	def traceToggle(self, _state):
		self.wSvgViewport.canvasUpdate(False)
		self.tracer.show(shapes=_state)
		self.wSvgViewport.canvasUpdate(True)

		Args.Viewport.visTracer = _state


### OPTIONS ###


	def prefsList(self):
		pinScheme = Args.Application.scheme

		wPrefs = PrefsWidget(self.wMain, Args._list())
		if not wPrefs.exec():
			return


		if Args.Application.scheme != pinScheme:
			self.sigPrefScheme.emit()
