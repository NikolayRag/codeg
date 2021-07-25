import os, logging

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *


class Object():
	None



class AppWindow():
	qApp = None

	args = None

	layout = Object()
	layout.main = None
	layout.canvas = None
	layout.btnOpen = None


	modulePath= os.path.abspath(os.path.dirname(__file__))



	def __init__(self, _args):
		self.args = _args

	def __init__(self):
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('plastique'))

		uiFile = os.path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');

		#capture widgets
		self.layout.canvas = cMain.findChild(QWidget, "canvasSVG")
		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		

		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)




	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()


# =todo 1 (feature) +0: load SVG



	def openFile(self, path=""):
		if path=="":
			fileName = QFileDialog.getOpenFileName(self.layout.main, "Open SVG File", "C:/", "*.svg")[0]
		else:
			fileName = path

