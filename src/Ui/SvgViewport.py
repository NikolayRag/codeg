from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import *

# =todo 32 (module-ui, spec, layout) +1: make isolated viewport widget
'''
Main scene widget
'''
class SvgViewport(QScrollArea):
	canvas = None

	pos = QPoint(0, 0)
	scale = 1.
	diff = 1.1



# =todo 4 (svg, feature) +0: zoom by wheel within center-mouse
# =todo 5 (svg, feature) +0: pan by mouse
#  todo 6 (svg, feature) +0: smooth animated zoom

	#mouse interaction
	def wheelEvent(self, _e):
		print(_e.pos())

		if self.canvas:
			self.scale *= self.diff if _e.delta()> 0 else 1/self.diff
			self.canvas.canvasSize(self.scale, self.scale)

		return True



	def mousePressEvent(self, _e):
		self.horizontalScrollBar().setValue( _e.pos().x() )
		self.verticalScrollBar().setValue( _e.pos().y() )

		return True



	def __init__(self, _parent):
		QScrollArea.__init__(self, _parent)

		self.setFrameShape(QFrame.NoFrame)



#####PUBLIC#####

	def addSVG(self, _xml):
		self.canvas = SvgCanvas(self, _xml)
		self.setWidget(self.canvas)



'''
Scene canvas 
'''
class SvgCanvas(QWidget):
	doc = None
	docWidth = 0
	docHeight = 0

	scaleX = 1.
	scaleY = 1.




	def __init__(self, parent, _xml):
		QWidget.__init__(self, parent)

		self.doc = QSvgRenderer(_xml, self)
		cSize = self.doc.defaultSize()
		self.docWidth = cSize.width()
		self.docHeight = cSize.height()



	def paintEvent(self, e):
		p = QPainter(self)
		p.setViewport( QRect(QPoint(0, 0), self.sizeHint()) )
		self.doc.render(p)



	def sizeHint(self):
		return QSize(
			self.docWidth * self.scaleX,
			self.docHeight * self.scaleY
		)



#####PUBLIC#####
	def canvasSize(self, _factorX, _factorY):
		self.scaleX = _factorX
		self.scaleY = _factorY

		self.resize(self.sizeHint())



