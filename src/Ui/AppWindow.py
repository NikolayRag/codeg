#  todo 33 (module-ui, widgets) +0: zoom slider
#  todo 34 (module-ui, widgets) +0: transform reset



import os, logging
import webbrowser

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

from .SvgViewport import *



class Object():
	None



class AppWindow():
	aboutHref = "https://github.com/NikolayRag/codeg"

	cbWFileLoad = None
	cbWFileSave = None
	cbWConnList = None

	qApp = None

	args = None

	layout = Object()
	layout.main = None
	layout.frameSVG = None
	layout.btnCaption = None
	layout.btnOpen = None
	layout.btnStore = None
	layout.ddPorts = None


	modulePath= os.path.abspath(os.path.dirname(__file__))



	def setCBFileLoad(self, _cb):
		self.cbWFileLoad = _cb



	def setCBFileSave(self, _cb):
		self.cbWFileSave = _cb



	def setCBConnList(self, _cb):
		self.cbWConnList = _cb

		self.connList()




	def __init__(self, _args):
		self.args = _args

		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))

		uiFile = os.path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');

		#capture widgets
		holderViewport = cMain.findChild(QFrame, "wViewport")
		self.layout.viewport = SvgViewport(holderViewport)
		holderViewport.layout().addWidget(self.layout.viewport)

		self.layout.btnCaption = cMain.findChild(QWidget, "btnCaption")
		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		self.layout.btnStore = cMain.findChild(QWidget, "btnSave")
		self.layout.ddPorts = cMain.findChild(QWidget, "ddPorts")


		cMain.connect(self.layout.btnCaption, SIGNAL("clicked()"), self.about)
		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)
		cMain.connect(self.layout.btnStore, SIGNAL("clicked()"), self.storeFile)
#		cMain.connect(self.layout.ddPorts, SIGNAL("clicked()"), self.connList)



	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()



	def about(self):
		webbrowser.open(self.aboutHref)



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



# =todo 46 (module-ui) +0: fill connection port list
	def connList(self):
		if not self.cbWConnList:
			return

		portsA = self.cbWConnList()

		for port in portsA:
			self.layout.ddPorts.insertItem(0,port)
