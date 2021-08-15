#  todo 36 (module-ui, API) +0: make viewport interaction callbacks

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *

# -todo 37 (module-ui, viewport) +0: make custom scrollbars out of SvgViewport

'''
Main scene widget
'''
class SvgViewport(QWidget):
	panOrigin = None

	panMargins = .2
	scaleMinPx = 10
	scaleMax = 10000


	canvas = None

	pos = QPoint(0, 0)
	scale = 1.
	diff = 1.1

	#screen space
	anchorCanvasX = .5
	anchorCanvasY = .5




#  todo 6 (module-ui, feature) +0: smooth animated zoom

	def resizeEvent(self, _e):
		if not self.canvas:
			return


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
			self.panOrigin = self.pos - _e.pos()



	def mouseMoveEvent(self, _e):
		if self.panOrigin:
			self.viewportPlace( self.panOrigin + _e.pos() )



	def mouseReleaseEvent(self, _e):
		if _e.button() == Qt.MouseButton.MiddleButton:
			self.panOrigin = None



	def viewportSize(self, _scale, _updateAnchor=True):
		if not self.canvas:
			return


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
		if not self.canvas:
			return


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



#####PUBLIC#####

	def isLoaded(self):
		return True if self.canvas else False



	def addSVG(self, _xml=None):
		if self.canvas:
			self.canvas.deleteLater()
			self.canvas = None


		if _xml:
			self.canvas = SvgCanvas(self, _xml, draw=False)
			self.canvasFit()
			self.canvasCenter()
			self.canvas.show()



	def changeSVG(self, _xml):
		self.canvas and self.canvas.replace(_xml)



	def canvasFit(self):
		if not self.canvas:
			return


		cSize = self.canvas.sizeHint()
		fitWidth = self.width() / cSize.width()
		fitHeight = self.height() / cSize.height()

		cScale = fitHeight if fitHeight<fitWidth else fitWidth
		self.viewportSize(cScale)



	def canvasCenter(self):
		if not self.canvas:
			return

		cSize = self.canvas.sizeHint()
		self.viewportPlace(QPoint(
			(self.width()-cSize.width())/2,
			(self.height()-cSize.height())/2
		))



'''
Scene canvas 
'''
class SvgCanvas(QWidget):
	doc = None
	docWidth = 0
	docHeight = 0

	
	offset = QPoint(0,0)

	scaleX = 1.
	scaleY = 1.




	def __init__(self, parent, _xml, draw=True):
		QWidget.__init__(self, parent)

		self.doc = QSvgRenderer(_xml, self)
		cSize = self.doc.defaultSize()
		self.docWidth = cSize.width()
		self.docHeight = cSize.height()

		if draw:
			self.update()



	def replace(self, _xml):
		self.doc.load(_xml)

		self.repaint()



	def paintEvent(self, e):
		p = QPainter(self)
		p.setViewport( QRect(QPoint(0, 0), self.sizeHint()) )
		self.doc.render(p)



	def sizeHint(self):
		return QSize(
			self.docWidth * self.scaleX,
			self.docHeight * self.scaleY
		)



	def update(self):
		self.resize(self.sizeHint())
		self.move(self.offset)

		QWidget.update(self)



#####PUBLIC#####
	def canvasSize(self, _factorX, _factorY):
		self.scaleX = _factorX
		self.scaleY = _factorY

		self.update()



	def canvasPlace(self, _offset):
		self.offset = _offset

		self.update()



	def getDocSize(self):
		return QSize(self.docWidth, self.docHeight)
