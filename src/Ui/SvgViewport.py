from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *



#  todo 37 (module-ui, viewport) +0: make custom scrollbars for SvgViewport
#  todo 229 (viewport, v2) +0: overview


#  todo 237 (svg, fix, v2) +0: go OGL

# =todo 239 (svg) +0: join SvgDescriptor and SvgCanvasLayer
class SvgDescriptor():
	canvas = None
	recomputeCB = None
	idGeo = -1


	def __init__(self, _canvas, _recomputeCB, _xml=None, z=0, ghost=False):
		self.canvas = _canvas
		self.recomputeCB = _recomputeCB
		self.idGeo = self.canvas.layerNew(z=z)

		self.ghost(ghost)

		if _xml:
			self.setXml(_xml)



	def setXml(self, _xml):
		self.canvas.layerSet(self.idGeo, _xml)

		self.recomputeCB()



	def place(self, _xy):
		self.canvas.layerSetOffset(self.idGeo, _xy)

		self.recomputeCB()



	def size(self, _xy):
		self.canvas.layerSetScale(self.idGeo, _xy)

		self.recomputeCB()



	def bbox(self):
		return self.canvas.layerBox(self.idGeo)



	def fit(self, _p1, _p2):
		xmm = sorted((_p1.x(), _p2.x()))
		ymm = sorted((_p1.y(), _p2.y()))
		self.place((xmm[0],ymm[0]))
		self.size((xmm[1]-xmm[0],ymm[1]-ymm[0]))



	def show(self, _vis):
		self.canvas.layerSetVis(self.idGeo, _vis)



	def ghost(self, _ghost):
		self.canvas.layerGhost(self.idGeo, _ghost)



	def static(self, _static):
		self.canvas.layerStatic(self.idGeo, _static)



#  todo 279 (viewport, fix) +0: make removed SvgDescriptor safe
	def remove(self):
		self.canvas.layerRemove(self.idGeo)



'''
Main scene widget
'''
class SvgViewport(QWidget):
	# sigInteract emit step conditions
	# intStart: left button pressed, storing start point for all other steps
	# intLive: mouse move while interacting
	# intEnd: left button released while interacting, stopping interaction
	# intCancel: right button pressed while interacting, stopping interaction
	# intOption: right button pressed alone
	intStart, intLive, intEnd, intCancel, intOption = (0,1,2,3,4)

	#step, coordTo, coordStart, keyModifiers, inspotFlag
	sigInteract = Signal(int, object, object, object, bool)


	prefs = type('', (object,), {
		'fit': .7,
		'offsetX': .66,
		'panMargins': .2,
		'scaleMin': 10,
		'scaleMax': 1000,
		'spotDist': 3,
		'zoomStep': 1.1,
	})


	#runtime
	canvas = None

	canvasPos = QPoint(0, 0)
	canvasScale = 1.
	canvasMidX = .5
	canvasMidY = .5


	#mouse events
	panOrigin = None
	interactStart = None
	interactKey = None
	interactSpot = True



#  todo 6 (module-ui, feature) -1: smooth animated zoom


	#mouse interaction
	def wheelEvent(self, _e):
		scaleMul = self.prefs.zoomStep if _e.delta()> 0 else 1/self.prefs.zoomStep

		oldScale = self.canvasScale
		self.viewportSize(self.canvasScale*scaleMul)

		posDelta = _e.pos() - self.canvasPos
		posDelta *= (1-self.canvasScale/oldScale)
		self.viewportPlace( self.canvasPos + posDelta )



	def mousePressEvent(self, _e):
		cPosTrue = QPointF(_e.pos() -self.canvasPos) / self.canvasScale


		if _e.button() == Qt.MouseButton.MiddleButton:
			self.panOrigin = _e.pos() -self.canvasPos


		if _e.button() == Qt.MouseButton.LeftButton:
			self.interactSpot = True
			self.interactKey = _e.modifiers()
			self.interactStart = cPosTrue
			self.sigInteract.emit(self.intStart, cPosTrue, self.interactStart, self.interactKey, True)


		if _e.button() == Qt.MouseButton.RightButton:
			if self.interactStart:
				self.sigInteract.emit(self.intCancel, cPosTrue, self.interactStart, self.interactKey, self.interactSpot)

			else:
				self.sigInteract.emit(self.intOption, cPosTrue, cPosTrue, _e.modifiers(), True)

			self.interactStart = None



	def mouseMoveEvent(self, _e):
		cPosTrue = QPointF(_e.pos() -self.canvasPos) / self.canvasScale


		if self.panOrigin:
			self.viewportPlace( _e.pos() - self.panOrigin)


		if self.interactStart:
			if (QLineF(self.interactStart, cPosTrue).length() *self.canvasScale)> self.prefs.spotDist:
				self.interactSpot = False

			self.sigInteract.emit(self.intLive, cPosTrue, self.interactStart, self.interactKey, self.interactSpot)



	def mouseReleaseEvent(self, _e):
		cPosTrue = QPointF(_e.pos() -self.canvasPos) / self.canvasScale


		if _e.button() == Qt.MouseButton.MiddleButton:
			self.panOrigin = None


		if _e.button() == Qt.MouseButton.LeftButton:
			if self.interactStart:
				self.sigInteract.emit(self.intEnd, cPosTrue, self.interactStart, self.interactKey, self.interactSpot)

			self.interactStart = None



	def resizeEvent(self, _e):
		oldW, oldH, newW, newH = _e.oldSize().width(), _e.oldSize().height(), _e.size().width(), _e.size().height()

		#portrait/landscape didnt change, use smallest side scale factor
		if (oldW-oldH)*(newW-newH)>0:
			cScale = (newW/oldW) if oldW<oldH else (newH/oldH)
		else:
			cScale = ( (newW/oldW)+(newH/oldH) ) /2.
		
		self.viewportSize(self.canvasScale*cScale, False)


		#compensate center position against viewport center
		cHint = self.canvas.getDocSize(self.canvasScale)
		self.viewportPlace( QPoint(
			round(newW*self.canvasMidX -cHint.width()*.5 -cHint.left()),
			round(newH*self.canvasMidY -cHint.height()*.5 -cHint.top())
		), False)



#  todo 95 (viewport, fix) +0: clip max scale by render limit
	def viewportSize(self, _scale, _updateAnchor=True):
		#max clip
		if _scale>self.prefs.scaleMax:
			_scale = self.prefs.scaleMax


		#min clip
		cSize = self.canvas.getDocSize(self.canvasScale)
		cWidth, cHeight = cSize.width(), cSize.height()
		newSize = (cWidth if cWidth<cHeight else cHeight) * _scale/self.canvasScale

		if self.prefs.scaleMin > newSize:
			_scale *= (self.prefs.scaleMin / newSize)


		self.canvasScale = _scale
		self.canvas.canvasSize(_scale, _scale)


		if _updateAnchor:
			self.anchorCanvas()



	def viewportPlace(self, _pos, _updateAnchor=True):
		cHint = self.canvas.getDocSize(self.canvasScale)

		cMarginX = self.width() * self.prefs.panMargins
		cMarginY = self.height() * self.prefs.panMargins

		if _pos.x() > (self.width() -cHint.left() -cMarginX):
			_pos.setX(self.width() -cHint.left() -cMarginX)
		if _pos.y() > (self.height() -cHint.top() -cMarginY):
			_pos.setY(self.height() -cHint.top() -cMarginY)


		if _pos.x() < (cMarginX -cHint.width() -cHint.left()):
			_pos.setX(cMarginX -cHint.width() -cHint.left())
		if _pos.y() < (cMarginY -cHint.height() -cHint.top()):
			_pos.setY(cMarginY -cHint.height() -cHint.top())


		self.canvasPos = _pos
		self.canvas.canvasPlace( _pos )


		if _updateAnchor:
			self.anchorCanvas()



	#hold canvas's midpoint in SvgViewport screen space
	# as cache for window resize
	def anchorCanvas(self):
		cHint = self.canvas.getDocSize(self.canvasScale)
		self.canvasMidX = ( self.canvasPos.x() +cHint.width()*.5 +cHint.left()) /self.width()
		self.canvasMidY = ( self.canvasPos.y() +cHint.height()*.5 +cHint.top()) /self.height()



	def __init__(self, _parent, _prefs=None):
		self.prefs = _prefs or self.prefs


		QWidget.__init__(self, _parent)

		QHBoxLayout(self)

		self.canvasReset()


#  todo 83 (ux, module-ui, fix) +0: fit at init dont work due to obsolete size 


#####PUBLIC#####


	def canvasReset(self):
		if self.canvas:
			self.canvas.setParent(None)
			self.canvas = None

		self.canvas = SvgCanvas(self)
		self.canvas.show()



	def canvasAdd(self, _xml=None, _offset=(0,0), _scale=(1,1), z=0, ghost=False):
		cDescr = SvgDescriptor(self.canvas, self.anchorCanvas, _xml, z=z, ghost=ghost)
		cDescr.place(_offset)
		cDescr.size(_scale)

		return cDescr



	def canvasFit(self, _box=None, _fit=None, _offset=None):
		cBox = QRectF(*_box) if _box else self.canvas.getDocSize()
		scaleX = self.width() / cBox.width()
		scaleY = self.height() / cBox.height()

		_fit = _fit or self.prefs.fit
		cScale = scaleY if scaleY<scaleX else scaleX
		self.viewportSize(cScale*_fit)


		#center
		_offset = _offset or self.prefs.offsetX
		self.viewportPlace(QPoint(
			self.width()*_offset -(cBox.left()+cBox.width()*_offset) *self.canvasScale,
			self.height()*.5 -(cBox.top()+cBox.height()*.5) *self.canvasScale
		))



	def canvasUpdate(self, _set=None):
		self.canvas.recompute(_set)



'''
Scene canvas 
'''
class SvgCanvasLayer(QSvgRenderer):
	z = 0
#	name = ''
	ghost = False
	display = True
#	lod = 1.


	scale = (1, 1)
	offset = (0, 0)
	static = False



	def __init__(self, _parent, z=0):
		QSvgRenderer.__init__(self, _parent)

		self.z = z



	def setGhost(self, _ghost):
		self.ghost = _ghost


	def setStatic(self, _static):
		self.static = _static



	def setDisplay(self, _display):
		self.display = _display



	def setLayerScale(self, _scale):
		self.scale = _scale


	def layerSize(self, _xs=1., _ys=1.):
		if not self.static:
			_xs = _ys = 1.

		defSize = self.defaultSize()
		if defSize.width()==-1 or defSize.height()==-1:
			return (0,0)
		return (defSize.width()*self.scale[0]/_xs, defSize.height()*self.scale[1]/_ys)



	def setLayerOffset(self, _offset):
		self.offset = _offset



	def layerOffset(self, _vpCompensate=False):
		if not _vpCompensate:
			return self.offset

		cpScale = [
			self.viewBox().width() / self.defaultSize().width(),
			self.viewBox().height() / self.defaultSize().height()
		]

		return [
			self.offset[0]-self.viewBox().x()/(cpScale[0] or 1),
			self.offset[1]-self.viewBox().y()/(cpScale[1] or 1)
		]



	def getLayerBox(self):
		return (*self.layerOffset(True), *self.layerSize())



	def zindex(self, _z=None):
		if _z != None:
			self.z = _z

		return self.z




class SvgCanvas(QWidget):
	defaultWidth = 0
	defaultHeight = 0

	layers = {}
	layerMaxId = 0
	docXMin = docXMax = docYMin = docYMax = 0
	ghostXMin = ghostXMax = ghostYMin = ghostYMax = 0

	updateEnabled = True

	
	offset = QPoint(0,0)

	scaleX = 1.
	scaleY = 1.


	def __init__(self, _parent, size=(1,1)):
		QWidget.__init__(self, _parent)

		self.layers = {}

		self.defaultWidth = size[0]
		self.defaultHeight = size[1]

# -todo 227 (fix) +0: integer pos and size result in SvgCanvasLayer jitter
		#anti jitter pin
		self.layers[-1] = SvgCanvasLayer(self, -1)
		self.layers[-1].setGhost(True)
		self.layers[-1].setLayerOffset((-10000,-10000))

		self.recompute()



	def layerNew(self, isGhost=False, z=0):
		cLayer = SvgCanvasLayer(self, z)
		cLayer.setGhost(isGhost)

		self.layerMaxId += 1
		self.layers[self.layerMaxId] = cLayer
		return self.layerMaxId



	def layerSet(self, _lId, _xml, quick=False):
		if not _xml:
			return

		cLayer = self.layers[_lId]
		cLayer.load(_xml)

		self.recompute()



	def layerSetOffset(self, _lId, _offset):
		cLayer = self.layers[_lId]
		cLayer.setLayerOffset(_offset)

		self.recompute()



	def layerSetScale(self, _lId, _scale):
		cLayer = self.layers[_lId]
		cLayer.setLayerScale(_scale)

		self.recompute()



	def layerBox(self, _lId):
		cLayer = self.layers[_lId]
		return cLayer.getLayerBox()



	def layerSetVis(self, _lId, _vis):
		cLayer = self.layers[_lId]
		cLayer.setDisplay(_vis)

		self.recompute()



	def layerGhost(self, _lId, _ghost):
		cLayer = self.layers[_lId]
		cLayer.setGhost(_ghost)

		self.recompute()



	def layerStatic(self, _lId, _static):
		cLayer = self.layers[_lId]
		cLayer.setStatic(_static)

		self.recompute()



	def layerRemove(self, _lId):
		del self.layers[_lId]

		self.recompute()



	def recompute(self, _set=None):
#  todo 286 (viewport, optimize) +0: recompute viewport nonblocking
		def runRe():
			defMinMax = ((0,), (self.defaultWidth,), (0,), (self.defaultHeight,))

			cLayers = list(self.layers.values())
			allLayerXforms = [[*l.layerOffset(True), *l.layerSize(self.scaleX,self.scaleY), l.ghost] for l in cLayers if l.display]

			minMax = tuple(zip(*[ [x, x+w, y, y+h] for x,y,w,h,g in allLayerXforms if not g]))
			minMax = minMax or defMinMax
			self.docXMin, self.docXMax = map(sorted(minMax[0]+minMax[1]).__getitem__, [0,-1])
			self.docYMin, self.docYMax = map(sorted(minMax[2]+minMax[3]).__getitem__, [0,-1])

			minMax = tuple(zip(*[ [x, x+w, y, y+h] for x,y,w,h,g in allLayerXforms if g]))
			minMax = minMax or defMinMax
			self.ghostXMin, self.ghostXMax = map(sorted(minMax[0]+minMax[1]+(self.docXMin,self.docXMax)).__getitem__, [0,-1])
			self.ghostYMin, self.ghostYMax = map(sorted(minMax[2]+minMax[3]+(self.docYMin,self.docYMax)).__getitem__, [0,-1])

			self.update()


		if _set != None:
			self.updateEnabled = _set

		if not self.updateEnabled:
			return


		runRe()



	def paintEvent(self, e):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)


		lOrdered = sorted(self.layers.values(), key=lambda l: l.zindex())
		for l in lOrdered:
			if not l.display:
				continue

			lSize = QSizeF(*l.layerSize(self.scaleX,self.scaleY))
			lPos = QPointF(*l.layerOffset())

			p.setViewport(
				(lPos.x()-self.ghostXMin) *self.scaleX, # compensate entire canvas offset
				(lPos.y()-self.ghostYMin) *self.scaleY,
				lSize.width() *self.scaleX,
				lSize.height() *self.scaleY
			)
			l.render(p)



	def sizeHint(self):
		return QSize(
			max(1, (self.ghostXMax - self.ghostXMin) * self.scaleX),
			max(1, (self.ghostYMax - self.ghostYMin) * self.scaleY)
		)



	def update(self):
		self.resize(self.sizeHint())
		self.move(QPoint(
			self.offset.x()+int(self.ghostXMin*self.scaleX),
			self.offset.y()+int(self.ghostYMin*self.scaleY)
		))

		QWidget.update(self)



	def canvasSize(self, _factorX, _factorY):
		self.scaleX = _factorX
		self.scaleY = _factorY

		self.update()



	def canvasPlace(self, _offset):
		self.offset = _offset

		self.update()



	def getDocSize(self, _scale=1):
		return QRectF(QPointF(self.docXMin,self.docYMin)*_scale, QPointF(self.docXMax, self.docYMax)*_scale)
