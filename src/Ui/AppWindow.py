import xml.etree.ElementTree as XML

import os, logging

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtSvg import *


class Object():
	None



class AppWindow():
	qApp = None

	args = None

	layout = Object()
	layout.main = None
	layout.frameSVG = None
	layout.btnOpen = None


	modulePath= os.path.abspath(os.path.dirname(__file__))



	def __init__(self, _args):
		self.args = _args

		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('plastique'))

		uiFile = os.path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');

		#capture widgets
		self.layout.frameSVG = cMain.findChild(QScrollArea, "scrollSVG")
		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		

		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)



	def buildSVG(self, _xml):
		view = SvgNativeView(_xml, self.layout.frameSVG)

		self.layout.frameSVG.setWidget(view)
		view.show()




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

		
		cSvg = XML.parse(fileName)

		self.buildSVG(XML.tostring(cSvg.getroot()))


		if cRecentA.count(fileName): cRecentA.remove(fileName)

		self.args.args["recentLoaded"] = cRecentA + [fileName]






'''
PySide2 example code template
'''
class SvgNativeView(QFrame):
	scale = 1.



	def __init__(self, _xml, parent):
		QFrame.__init__(self, parent)

		self.doc = QSvgRenderer(_xml, self)
		cSize = self.doc.defaultSize()
		self.docWidth = cSize.width()
		self.docHeight = cSize.height()

		self.connect(self.doc, SIGNAL("repaintNeeded()"),
			self, SLOT("update()"))



	def paintEvent(self, e):
		p = QPainter(self)
		p.setViewport( QRect(QPoint(0, 0), self.sizeHint()) )
		self.doc.render(p)



	def sizeHint(self):
		return QSize(
			self.docWidth * self.scale,
			self.docHeight * self.scale
		)



#  todo 4 (svg, feature) +0: zoom by wheel
#  todo 5 (svg, feature) +0: pan by mouse
#  todo 6 (svg, feature) +0: smooth animated zoom

	def wheelEvent(self, e):
		diff = 1.1
		self.setScale(self.scale * (diff if e.delta()> 0 else 1/diff))



	def setScale(self, _scale):
		self.scale = _scale

		self.resize(self.sizeHint())

