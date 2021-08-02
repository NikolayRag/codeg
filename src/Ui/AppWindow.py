#  todo 28 (module-ui) +0: add credits: About, License, Github

import os, logging

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtSvg import *


class Object():
	None



class AppWindow():
	cbWFileLoad = None
	cbWFileSave = None

	qApp = None

	args = None

	layout = Object()
	layout.main = None
	layout.frameSVG = None
	layout.btnOpen = None
	layout.btnStore = None


	modulePath= os.path.abspath(os.path.dirname(__file__))



	def setCBFileLoad(self, _cb):
		self.cbWFileLoad = _cb



	def setCBFileSave(self, _cb):
		self.cbWFileSave = _cb



	def __init__(self, _args):
		self.args = _args

		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('plastique'))

		uiFile = os.path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');

		#capture widgets
		holderViewport = cMain.findChild(QFrame, "wViewport")
		self.layout.viewport = GGViewport(holderViewport)
		holderViewport.layout().addWidget(self.layout.viewport)

		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		self.layout.btnStore = cMain.findChild(QWidget, "btnSave")
		


		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)
		cMain.connect(self.layout.btnStore, SIGNAL("clicked()"), self.storeFile)




	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()


#  todo 3 (feature, file) +0: allow picking from Recent files list

	def openFile(self):
		cRecentA = self.args.args["recentLoaded"] if ("recentLoaded" in self.args.args) else []

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(self.layout.main, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if not self.cbWFileLoad:
			print('No load CB')
			return

		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.args["recentLoaded"] = cRecentA + [fileName]


		cData = self.cbWFileLoad(fileName)
		self.layout.viewport.addSVG(cData)
		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeFile(self):
		if not self.cbWFileSave:
			print('No save CB')
			return

		cRecentA = self.args.args["recentSaved"] if ("recentSaved" in self.args.args) else []

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(self.layout.main, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		self.cbWFileSave(fileName)


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.args["recentSaved"] = cRecentA + [fileName]






'''
Main scene widget
'''
class GGViewport(QScrollArea):
	canvas = None

	pos = QPoint(0, 0)
	scale = 1.
	diff = 1.1



	#mouse interaction
	def wheelEvent(self, _e):
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



#  todo 4 (svg, feature) +0: zoom by wheel within center-mouse
#  todo 5 (svg, feature) +0: pan by mouse
#  todo 6 (svg, feature) +0: smooth animated zoom

#####PUBLIC#####
	def canvasSize(self, _factorX, _factorY):
		self.scaleX = _factorX
		self.scaleY = _factorY

		self.resize(self.sizeHint())



