#  todo 33 (module-ui, widgets) +0: zoom slider
#  todo 34 (module-ui, widgets) +0: transform reset


import re
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



'''
Viewport dispatch OSD
'''
#  todo 271 (ux, clean) +0: trace detailed stats
# =todo 272 (ux, clean) +0: trace show error/warning position
#  todo 273 (ux, clean) +0: rewindable trace history
#  todo 274 (ux, clean) +0: make paint nonblocking
class Tracer():
	pointTrace = 'resource\\point-trace.svg'

	outHeadInter = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#590' stroke-dasharray='3' fill='none' points='"
	outHeadShape = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#3b0' fill='none' points='"

	decayDraw = 100.


	canvas = None
	focus = None
	spots = None
	osd = None


	session = None

	canvasVBox = None
	canvasBody = []
	canvasSpots = []

	visible = True


	def __init__(self, _svgGen, _osd=None):
		self.canvas = _svgGen(0)
		self.canvas.ghost(True)

		self.focus = _svgGen(1)
		self.focus.setXml(self.pointTrace)
		self.focus.ghost(True)
		self.focus.static(True)

		self.spots = _svgGen(2)
		self.spots.ghost(True)
#		self.spots.static(True)

		self.osd = _osd



	def show(self, _state):
		self.visible = _state
		if _state and self.canvasVBox:
			self.canvasBuild()


		self.canvas.show(_state)
		self.focus.show(_state)
		self.spots.show(_state)



	def reset(self, _session):
		self.session = _session

		self.canvasVBox = _session.viewBox()
		self.canvasBody = [[]]
		self.canvasSpots = []

		self.canvas.place(self.canvasVBox[0:2])
		self.canvasBuild([0,0])
		
		self.spots.place(self.canvasVBox[0:2])



	def feed(self, _res, _cmd):
		edge = re.findall("S[\d]+", _cmd)
		if len(edge)==1 and float(edge[0][1:])==0:
			self.canvasBuild()
			self.canvasBody.append([])


		coords = re.findall("[XY]-?[\d\.]+", _cmd)

		if len(coords)==2 and len(coords[0])>1 and len(coords[1])>1 and coords[0][0]=='X' and coords[1][0]=='Y':
			self.moveto(float(coords[0][1:]), -float(coords[1][1:]))


		l = sum(len(x) for x in self.canvasBody)
		progress = round(100.*l/self.session.pathLen(),2)
		step = int(l/self.decayDraw)+1

		if _res != True:
			col = '#bb0' if _res else '#f00'
			self.canvasSpots += [f"<circle cx='{float(coords[0][1:])-self.canvasVBox[0]}' cy='{-float(coords[1][1:])-self.canvasVBox[1]}' r='1px' vector-effect='non-scaling-stroke' stroke='{col}' fill='{col}' stroke-width='3px'/>"]

			cSpot = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
			for sp in self.canvasSpots:
				cSpot += [sp]
			cSpot += ["</svg>"]

			self.spots.setXml(' '.join(cSpot).encode())

			print(f'Step {l}/{step}: {progress}% with {_res}')



	def final(self, _res):
		self.canvasBuild()



	def moveto(self, _x, _y):
		self.focus and self.focus.place((_x, _y))

		self.canvasBuild((_x,_y))



	def canvasBuild(self, _add=None):
		if _add:
			self.canvasBody[-1] += [f"{_add[0]-self.canvasVBox[0]},{_add[1]-self.canvasVBox[1]}"]

		l = sum(len(x) for x in self.canvasBody)
		if _add and (not self.visible or (l% (int(l/self.decayDraw)+1))):
			return


		last = None

#  todo 269 (module-ui, clean, fix) +1: make painting reasonable
		out = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
		for sh in self.canvasBody:
			if last:
				out += [self.outHeadInter] + last + [sh[0]] + ["'/>"]

			out += [self.outHeadShape] + sh + ["'/>"]

			last = [sh[-1]]

		out += ["</svg>"]

		self.canvas.setXml(' '.join(out).encode())



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
		self.wBtnTraceView.setChecked(Args.Viewport.traceLayer)

		self.wBtnCaption = cMain.findChild(QWidget, "btnCaption")
		self.wBtnWipe = cMain.findChild(QWidget, "btnWipe")
		self.wBtnOpen = cMain.findChild(QWidget, "btnOpen")
		self.wBtnSave = cMain.findChild(QWidget, "btnSave")
		self.wBtnLoad = cMain.findChild(QWidget, "btnLoad")
		self.wBtnDispShot = cMain.findChild(QWidget, "btnDispShot")
		self.wBtnPaste = cMain.findChild(QWidget, "btnPaste")
		self.wBtnPrefs = cMain.findChild(QWidget, "btnPrefs")

		self.wFrameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.wFrameDispatcher.setVisible(False)
#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.wBtnRescan = cMain.findChild(QWidget, "btnRescan")
		self.wListDevs = cMain.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = cMain.findChild(QWidget, "btnDispFire")
		self.wFrameDev = cMain.findChild(QPlainTextEdit, "frameDev")


		self.wBtnFit.clicked.connect(self.viewportFit)
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



	def traceSet(self, data, start=False):
		if start:
			self.wFrameDev.appendPlainText("Dispatch new session\n")
			self.tracer.reset(data)

			return


		self.wFrameDev.appendPlainText(f"Dispatch {'ok' if data else 'error'}\n")
		self.tracer.final(data)



	def traceFeed(self, _res, _echo):
		self.wFrameDev.appendPlainText(('+' if _res==True else f"  {_res or 'Warning'}:\n- ") + _echo)
		self.tracer.feed(_res, _echo)



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

		self.tracer = Tracer(lambda z:self.wSvgViewport.canvasAdd(z=100+z))
		self.traceToggle(Args.Viewport.traceLayer)



	def gridSize(self, _size):
		self.gridDescription.size(_size)
		self.gridDescription.place((0,-_size[1]))



	def traceToggle(self, _state):
		self.tracer.show(_state)
		Args.Viewport.traceLayer = _state



### OPTIONS ###


	def prefsList(self):
		pinScheme = Args.Application.scheme

		wPrefs = PrefsWidget(self.wMain, Args._list())
		if not wPrefs.exec():
			return


		if Args.Application.scheme != pinScheme:
			self.sigPrefScheme.emit()
