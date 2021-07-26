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



	def buildSVG(self, _fn):
		view = SvgNativeView(_fn, self.layout.frameSVG)

		self.layout.frameSVG.setWidget(view)
		view.show()




	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()


# =todo 1 (feature) +0: load SVG



	def openFile(self):
		cRecentA = self.args.args["recentLoaded"] if ("recentLoaded" in self.args.args) else []

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(self.layout.main, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		self.buildSVG(fileName)


		if cRecentA.count(fileName): cRecentA.remove(fileName)

		self.args.args["recentLoaded"] = cRecentA + [fileName]






'''
PySide2 example code template
'''
class SvgNativeView(QFrame):

    def __init__(self, path, parent):
        QFrame.__init__(self, parent)

        self.doc = QSvgRenderer(path, self)
        self.connect(self.doc, SIGNAL("repaintNeeded()"),
                     self, SLOT("update()"))



    def paintEvent(self, e):
        p = QPainter(self)
        p.setViewport(0, 0, self.width(), self.height())
        self.doc.render(p)



    def sizeHint(self):
        if self.doc:
            return self.doc.defaultSize()
        return QWidget.sizeHint(self)
