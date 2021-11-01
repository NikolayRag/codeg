from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *



#  todo 37 (module-ui, viewport) +0: make custom scrollbars for SvgViewport
#  todo 229 (viewport, v2) +0: overview


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



	def place(self, _xy):
		self.canvas.layerSetOffset(self.idGeo, _xy)



	def size(self, _xy):
		self.canvas.layerSetScale(self.idGeo, _xy)



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


	panMargins = .2
	scaleMinPx = 10
	scaleMax = 10000
	spotDist = 10
	zoomStep = 1.1


	#runtime
	canvas = None

	canvasPos = QPoint(0, 0)
	canvasScale = 1.
	zoomAnchorX = .5
	zoomAnchorY = .5


	#mouse events
	panOrigin = None
	interactStart = None
	interactKey = None
	interactSpot = True



#  todo 6 (module-ui, feature) -1: smooth animated zoom


	def resizeEvent(self, _e):
		oldW, oldH, newW, newH = _e.oldSize().width(), _e.oldSize().height(), _e.size().width(), _e.size().height()

		#portrait/landscape didnt change, use smallest side scale factor
		if (oldW-oldH)*(newW-newH)>0:
			cScale = (newW/oldW) if oldW<oldH else (newH/oldH)
		else:
			cScale = ( (newW/oldW)+(newH/oldH) ) /2.
		
		self.viewportSize(self.canvasScale*cScale, False)


		#compensate center position against viewport center
		newHint = self.canvas.sizeHint()
		self.viewportPlace( QPoint(
			round(self.zoomAnchorX*newW - newHint.width()*.5),
			round(self.zoomAnchorY*newH - newHint.height()*.5)
		), False)



	#mouse interaction
	def wheelEvent(self, _e):
		scaleMul = self.zoomStep if _e.delta()> 0 else 1/self.zoomStep

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
			if (QLineF(self.interactStart, cPosTrue).length() *self.canvasScale)> self.spotDist:
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



#  todo 95 (viewport, fix) +0: clip max scale by render limit
	def viewportSize(self, _scale, _updateAnchor=True):
		#max clip
		if _scale>self.scaleMax:
			_scale = self.scaleMax


		#min clip
		cSize = self.canvas.sizeHint()
		cWidth, cHeight = cSize.width(), cSize.height()
		newSize = (cWidth if cWidth<cHeight else cHeight) * _scale/self.canvasScale

		if self.scaleMinPx > newSize:
			_scale *= (self.scaleMinPx / newSize)


		self.canvasScale = _scale
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


		self.canvasPos = _pos
		self.canvas.canvasPlace( _pos )


		if _updateAnchor:
			self.anchorCanvas()



	#hold canvas's midpoint in SvgViewport screen space
	# as cache for window resize
	def anchorCanvas(self):
		cHint = self.canvas.sizeHint()
		self.zoomAnchorX = ( self.canvasPos.x()+cHint.width()*.5 ) /self.width()
		self.zoomAnchorY = ( self.canvasPos.y()+cHint.height()*.5 ) /self.height()



	def __init__(self, _parent):
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



	def canvasAdd(self, _xml=None, _offset=(0,0)):
		cDescr = SvgDescriptor(self.canvas, _xml)
		cDescr.place(_offset)

		return cDescr



	def canvasFit(self, multiply=1., offset=.5):
# -todo 156 (fix, canvas) +0: canvas is wrong size at init
		cBox = self.canvas.getDocSize()
		scaleX = self.width() / cBox.width()
		scaleY = self.height() / cBox.height()

#  todo 226 (fix, check) +0: probably will fit wrong if canvas and widget orientation differs
		cScale = scaleY if scaleY<scaleX else scaleX
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


	scale = (1, 1)
	offset = (0, 0)


	def __init__(self, _parent):
		QSvgRenderer.__init__(self, _parent)



	def setGhost(self, _ghost):
		self.ghost = _ghost



	def setDisplay(self, _display):
		self.display = _display



	def setLayerScale(self, _scale):
		self.scale = _scale


	def layerSize(self):
		defSize = self.defaultSize()
		return QSizeF(defSize.width()*self.scale[0], defSize.height()*self.scale[1])



	def setLayerOffset(self, _offset):
		self.offset = _offset



	def layerOffset(self):
		return QPointF(*self.offset)




# =todo 227 (fix) +0: integer pos and size result in jitter
class SvgCanvas(QWidget):
	defaultWidth = 0
	defaultHeight = 0

	layers = {}
	layerMaxId = 0
	docXMin = 0
	docXMax = 0
	docYMin = 0
	docYMax = 0

	
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

		self.recompute()



	def layerSetOffset(self, _lId, _offset):
		cLayer = self.layers[_lId]
		cLayer.setLayerOffset(_offset)

		self.recompute()



	def layerSetScale(self, _lId, _scale):
		cLayer = self.layers[_lId]
		cLayer.setLayerScale(_scale)

		self.recompute()



	def recompute(self, _update=True):
			if not self.layers:
				self.docXMin = 0
				self.docXMax = self.defaultWidth
				self.docYMin = 0
				self.docYMax = self.defaultHeight


				if _update:
					self.update()

				return


			f = True
			for l in self.layers.values():
				if not l.display:
					continue

				lSize = l.layerSize()
				lPos = l.layerOffset()

				if f:
					f = False
					self.docXMin = lPos.x()
					self.docXMax = lSize.width() +lPos.x()
					self.docYMin = lPos.y()
					self.docYMax = lSize.height() +lPos.y()

				else:
					self.docXMin = min(self.docXMin, lPos.x())
					self.docXMax = max(self.docXMax, lSize.width()+lPos.x())
					self.docYMin = min(self.docYMin, lPos.y())
					self.docYMax = max(self.docYMax, lSize.height()+lPos.y())


			if _update:
				self.update()



	def paintEvent(self, e):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)


		for l in self.layers.values():
			if not l.display:
				continue

			lSize = l.layerSize()
			lPos = l.layerOffset()

			p.setViewport(
				(lPos.x()-self.docXMin) *self.scaleX, # compensate entire canvas offset
				(lPos.y()-self.docYMin) *self.scaleY,
				lSize.width() *self.scaleX,
				lSize.height() *self.scaleY
			)
			l.render(p)



	def sizeHint(self):
		return QSize(
			max(1, (self.docXMax - self.docXMin) * self.scaleX),
			max(1, (self.docYMax - self.docYMin) * self.scaleY)
		)



	def update(self):
		self.resize(self.sizeHint())
		self.move(QPoint(
			self.offset.x()+int(self.docXMin*self.scaleX),
			self.offset.y()+int(self.docYMin*self.scaleY)
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
