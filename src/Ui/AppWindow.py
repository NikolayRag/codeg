from os import path

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *


class Object():
	None



class AppWindow():
	qApp = None

	layout = Object()
	layout.main = None

	modulePath= path.abspath(path.dirname(__file__))



	def __init__(self):
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('plastique'))

		uiFile = path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)


		#capture widgets
#		self.layout.drag= cMain.findChild(QWidget, "outerFrame")

		




	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()



