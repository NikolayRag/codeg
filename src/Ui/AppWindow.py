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
		self.layout.frameSVG = cMain.findChild(QScrollArea, "scrollSVG")
		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		self.layout.btnStore = cMain.findChild(QWidget, "btnSave")
		

		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)
		cMain.connect(self.layout.btnStore, SIGNAL("clicked()"), self.storeFile)



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

		
		if not self.cbWFileLoad:
			print('No load CB')
			return

		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.args["recentLoaded"] = cRecentA + [fileName]


		cData = self.cbWFileLoad(fileName)
		self.buildSVG(cData)

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

