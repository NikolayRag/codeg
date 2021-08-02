from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *

# =todo 32 (module-ui, spec, layout) +1: make isolated viewport widget
'''
Main scene widget
'''
class SvgViewport(QWidget):
	panMargins = 50

	canvas = None

	pos = QPoint(0, 0)
	scale = 1.
	diff = 1.1



# =todo 4 (svg, feature) +0: zoom by wheel within center-mouse
# =todo 5 (svg, feature) +0: pan by mouse
#  todo 6 (svg, feature) +0: smooth animated zoom

	#mouse interaction
	def wheelEvent(self, _e):
		scaleMul = self.diff if _e.delta()> 0 else 1/self.diff

		self.viewportSize(self.scale*scaleMul)

		posDelta = _e.pos() - self.pos
		posDelta *= (1-scaleMul)
		self.viewportPlace( self.pos + posDelta )



	def mousePressEvent(self, _e):
		self.viewportPlace( _e.pos() )



	def viewportSize(self, _scale):
		if not self.canvas:
			return


		self.canvas.canvasSize(_scale, _scale)

		self.scale = _scale



	def viewportPlace(self, _pos):
		if not self.canvas:
			return


		cSize = self.canvas.sizeHint()

		if _pos.x()>(self.width()-self.panMargins):
			_pos.setX(self.width()-self.panMargins)
		if _pos.y()>(self.height()-self.panMargins):
			_pos.setY(self.height()-self.panMargins)

		if _pos.x()<(self.panMargins-cSize.width()):
			_pos.setX(self.panMargins-cSize.width())
		if _pos.y()<(self.panMargins-cSize.height()):
			_pos.setY(self.panMargins-cSize.height())


		self.pos = _pos
		self.canvas.canvasPlace( _pos )




	def __init__(self, _parent):
		QWidget.__init__(self, _parent)

		QHBoxLayout(self)


#####PUBLIC#####

	def addSVG(self, _xml=None):
		if self.canvas:
			self.canvas.deleteLater()
			self.canvas = None


		if _xml:
			self.canvas = SvgCanvas(self, _xml)
			self.canvasFit()
			self.canvasCenter()
			self.canvas.show()



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




	def __init__(self, parent, _xml):
		QWidget.__init__(self, parent)

		self.doc = QSvgRenderer(_xml, self)
		cSize = self.doc.defaultSize()
		self.docWidth = cSize.width()
		self.docHeight = cSize.height()

		self.update()



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
