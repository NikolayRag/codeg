from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *



#  todo 37 (module-ui, viewport) +0: make custom scrollbars for SvgViewport
#  todo 207 (viewport, v2) +0: onscreen controls


class SvgDescriptor():
	canvas = None
	idGeo = -1


	def __init__(self, _canvas, _xml=None):
		self.canvas = _canvas
		self.idGeo = self.canvas.layerNew()

		if _xml:
			self.setXml(_xml)



	def setXml(self, _xml):
		self.canvas.layerSet(self.idGeo, _xml)



'''
Main scene widget
'''
class SvgViewport(QWidget):
	sigInteract = Signal(object, object)

	eventTypes = {}


	panOrigin = None

	panMargins = .2
	scaleMinPx = 10
	scaleMax = 10000


	gridXml = None
	canvas = None

	layerId = -1

	pos = QPoint(0, 0)
	scale = 1.
	diff = 1.1

	#screen space
	anchorCanvasX = .5
	anchorCanvasY = .5


	#runtime

	interactStart = None



#  todo 6 (module-ui, feature) -1: smooth animated zoom


	def resizeEvent(self, _e):
		oldW, oldH, newW, newH = _e.oldSize().width(), _e.oldSize().height(), _e.size().width(), _e.size().height()

		#portrait/landscape didnt change, use smallest side scale factor
		if (oldW-oldH)*(newW-newH)>0:
			cScale = (newW/oldW) if oldW<oldH else (newH/oldH)
		else:
			cScale = ( (newW/oldW)+(newH/oldH) ) /2.
		
		self.viewportSize(self.scale*cScale, False)


		#compensate center position against viewport center
		newHint = self.canvas.sizeHint()
		self.viewportPlace( QPoint(
			round(self.anchorCanvasX*newW - newHint.width()*.5),
			round(self.anchorCanvasY*newH - newHint.height()*.5)
		), False)



	#mouse interaction
	def wheelEvent(self, _e):
		scaleMul = self.diff if _e.delta()> 0 else 1/self.diff

		oldScale = self.scale
		self.viewportSize(self.scale*scaleMul)

		posDelta = _e.pos() - self.pos
		posDelta *= (1-self.scale/oldScale)
		self.viewportPlace( self.pos + posDelta )



	def mousePressEvent(self, _e):
		if _e.button() == Qt.MouseButton.MiddleButton:
			self.panOrigin = _e.pos() - self.pos


		if _e.button() == Qt.MouseButton.LeftButton:
			self.interactStart = _e.pos() - self.pos

		if _e.button() == Qt.MouseButton.RightButton:
			self.interactStart = None



	def mouseMoveEvent(self, _e):
		if self.panOrigin:
			self.viewportPlace( _e.pos() - self.panOrigin)



	def mouseReleaseEvent(self, _e):
		if _e.button() == Qt.MouseButton.MiddleButton:
			self.panOrigin = None


		if _e.button() == Qt.MouseButton.LeftButton:
			if self.interactStart:
				interactEnd = _e.pos()-self.pos
				self.sigInteract.emit(
					self.interactStart,
					interactEnd
				)

			self.interactStart = None



#  todo 95 (viewport, fix) +0: clip max scale by render limit
	def viewportSize(self, _scale, _updateAnchor=True):
		#max clip
		if _scale>self.scaleMax:
			_scale = self.scaleMax


		#min clip
		cSize = self.canvas.sizeHint()
		cWidth, cHeight = cSize.width(), cSize.height()
		newSize = (cWidth if cWidth<cHeight else cHeight) * _scale/self.scale

		if self.scaleMinPx > newSize:
			_scale *= (self.scaleMinPx / newSize)


		self.scale = _scale
		self.canvas.canvasSize(_scale, _scale)


		if _updateAnchor:
			self.anchorCanvas()



	def viewportPlace(self, _pos, _updateAnchor=True):
		cSize = self.canvas.sizeHint()

		cMarginX = self.width() * self.panMargins
		cMarginY = self.height() * self.panMargins

		if _pos.x()>(self.width()-cMarginX):
			_pos.setX(self.width()-cMarginX)
		if _pos.y()>(self.height()-cMarginY):
			_pos.setY(self.height()-cMarginY)


		if _pos.x()<(cMarginX-cSize.width()):
			_pos.setX(cMarginX-cSize.width())
		if _pos.y()<(cMarginY-cSize.height()):
			_pos.setY(cMarginY-cSize.height())


		self.pos = _pos
		self.canvas.canvasPlace( _pos )


		if _updateAnchor:
			self.anchorCanvas()



	#hold canvas's midpoint in SvgViewport screen space
	# as cache for window resize
	def anchorCanvas(self):
		cHint = self.canvas.sizeHint()
		self.anchorCanvasX = ( self.pos.x()+cHint.width()*.5 ) /self.width()
		self.anchorCanvasY = ( self.pos.y()+cHint.height()*.5 ) /self.height()



	def __init__(self, _parent):
		QWidget.__init__(self, _parent)

		QHBoxLayout(self)

		self.canvasReset()


# -todo 89 (ux, module-ui, fix) +0: place grid correctly
#  todo 83 (ux, module-ui, fix) +0: fit at init dont work due to obsolete size 


#####PUBLIC#####



	def setGrid(self, _gridXml=None):
		self.gridXml = _gridXml



	def canvasReset(self):
		if self.canvas:
			self.canvas.deleteLater()
			self.canvas = None

		self.canvas = SvgCanvas(self)
		self.canvas.show()

		if self.gridXml:
			self.canvas.layerSet(self.canvas.layerNew(True), self.gridXml)



	def canvasAdd(self, _xml=None):
		return SvgDescriptor(self.canvas, _xml)



	def canvasFit(self, multiply=1., offset=.5):
# -todo 156 (fix, canvas) +0: canvas is wrong size at init
		fitWidth = self.width() / self.canvas.docWidth
		fitHeight = self.height() / self.canvas.docHeight


		cScale = fitHeight if fitHeight<fitWidth else fitWidth
		self.viewportSize(cScale*multiply)


		#place
		cSize = self.canvas.sizeHint()
		self.viewportPlace(QPoint(
			(self.width()-cSize.width())*offset,
			(self.height()-cSize.height())*.5
		))



'''
Scene canvas 
'''
class SvgCanvasLayer(QSvgRenderer):
#	name = ''
	ghost = False
	display = True
#	lod = 1.


	def __init__(self, _parent):
		QSvgRenderer.__init__(self, _parent)


	def setGhost(self, _ghost):
		self.ghost = _ghost


	def setDisplay(self, _display):
		self.display = _display



class SvgCanvas(QWidget):
	defaultWidth = 0
	defaultHeight = 0

	layers = {}
	layerMaxId = 0
	docWidth = 0
	docHeight = 0

	
	offset = QPoint(0,0)

	scaleX = 1.
	scaleY = 1.


	def __init__(self, _parent, size=(1,1)):
		QWidget.__init__(self, _parent)

		self.layers = {}

		self.defaultWidth = size[0]
		self.defaultHeight = size[1]

		self.recompute()



	def layerNew(self, isGhost=False):
		cLayer = SvgCanvasLayer(self)
		cLayer.setGhost(isGhost)

		self.layerMaxId += 1
		self.layers[self.layerMaxId] = cLayer
		return self.layerMaxId



	def layerSet(self, _lId, _xml, quick=False):
		if not _xml:
			return

		cLayer = self.layers[_lId]
		cLayer.load(_xml)

		if quick:
			self.repaint()
		else:
			self.recompute()

			self.update()



	def recompute(self):
			self.docWidth = 0
			self.docHeight = 0

			for l in self.layers.values():
				if l.display and not l.ghost:
					cSize = l.defaultSize()
					self.docWidth = max(self.docWidth, cSize.width())
					self.docHeight = max(self.docHeight, cSize.height())


			if not self.docWidth:
				self.docWidth = self.defaultWidth
			if not self.docHeight:
				self.docHeight = self.defaultHeight



	def paintEvent(self, e):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)

		for l in self.layers.values():
			if not l.display:
				continue
#  todo 97 (viewport, fix, solve) +0: decide how to paint different layer sizes
			p.setViewport( QRect(QPoint(0, 0), self.sizeHint()) )
			l.render(p)



	def sizeHint(self):
		return QSize(
			self.docWidth * self.scaleX,
			self.docHeight * self.scaleY
		)



	def update(self):
		self.resize(self.sizeHint())
		self.move(self.offset)

		QWidget.update(self)



	def canvasSize(self, _factorX, _factorY):
		self.scaleX = _factorX
		self.scaleY = _factorY

		self.update()



	def canvasPlace(self, _offset):
		self.offset = _offset

		self.update()



	def getDocSize(self):
		return QSize(self.docWidth, self.docHeight)
