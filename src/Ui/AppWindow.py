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
	cbWDispatch = None
	cbWLayerPick = None


	qApp = None

	args = None

	layout = Object()
	layout.main = None
	layout.viewport = None
	layout.listLayers = None
	layout.frameSVG = None
	layout.btnCaption = None
	layout.btnOpen = None
	layout.btnStore = None
	layout.ddPorts = None


	modulePath= os.path.abspath(os.path.dirname(__file__))


	recentLayersSelected = list()



	def setCBFileLoad(self, _cb):
		self.cbWFileLoad = _cb



	def setCBFileSave(self, _cb):
		self.cbWFileSave = _cb



	def setCBLayerPick(self, _cb):
		self.cbWLayerPick = _cb



	def setCBConnList(self, _cb):
		self.cbWConnList = _cb

		self.connList()



	def setCBDispatch(self, _cb):
		self.cbWDispatch = _cb



	def __init__(self, _args):
		self.args = _args

		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))
#  todo 50 (module-ui) +0: add style
#		with open('Ui/style.qss') as fQss:
#			self.qApp.setStyleSheet(fQss.read())

		uiFile = os.path.join(self.modulePath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');

		#capture widgets
		self.layout.listLayers = cMain.findChild(QTableWidget, "listLayers")
		self.layout.listLayers.setEditTriggers(QAbstractItemView.NoEditTriggers);

		holderViewport = cMain.findChild(QFrame, "wViewport")
		self.layout.viewport = SvgViewport(holderViewport)
		holderViewport.layout().addWidget(self.layout.viewport)

		self.layout.btnCaption = cMain.findChild(QWidget, "btnCaption")
		self.layout.btnOpen = cMain.findChild(QWidget, "btnLoad")
		self.layout.btnStore = cMain.findChild(QWidget, "btnSave")

		self.layout.frameDispatcher = cMain.findChild(QWidget, "frameDispatcher")
		self.layout.frameDispatcher.setVisible(False)
#  todo 47 (module-dispatch, module-ui, ux) +0: change device list to button+list
#  todo 48 (module-ui) +0: update device list
#  todo 49 (module-ui, ux) +0: save/restore active device between sessions
		self.layout.ddPorts = cMain.findChild(QWidget, "ddPorts")
		self.layout.btnProccess = cMain.findChild(QWidget, "btnProccess")


		cMain.connect(self.layout.btnCaption, SIGNAL("clicked()"), self.about)
		cMain.connect(self.layout.btnOpen, SIGNAL("clicked()"), self.openFile)
		cMain.connect(self.layout.btnStore, SIGNAL("clicked()"), self.storeFile)
		cMain.connect(self.layout.listLayers, SIGNAL("itemSelectionChanged()"), self.layerPick)
		cMain.connect(self.layout.btnProccess, SIGNAL("clicked()"), self.dispatchRun)



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
		if not self.cbWFileLoad:
			print('No load CB')
			return


		cData = self.cbWFileLoad()
		if cData:
			self.layout.btnStore.setEnabled(True)
			self.layout.btnProccess.setEnabled(True)

			self.layout.viewport.addSVG(cData['xml'])


			cList = self.layout.listLayers
			cList.setRowCount(0)
			cRow = 0

			for cItem in cData['meta']:
				cList.insertRow(cRow)
				cList.setItem(cRow, 0, QTableWidgetItem(cItem))
				cRow += 1

		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeFile(self):
		if not self.cbWFileSave:
			print('No save CB')
			return


		self.cbWFileSave()



	def layerPick(self):
		if not self.cbWLayerPick:
			print('No layer CB')
			return


#  todo 53 (fix, module-ui) +0: reset layers selection at reload
		for cRange in self.recentLayersSelected:
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cName = self.layout.listLayers.item(cRow,0)
				self.cbWLayerPick(cName.text(), False)


		self.recentLayersSelected = self.layout.listLayers.selectedRanges()
		
		for cRange in self.recentLayersSelected:
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				cName = self.layout.listLayers.item(cRow,0)
				self.cbWLayerPick(cName.text(), True)


		cXml = self.cbWLayerPick()
		self.layout.viewport.changeSVG(cXml)




	def connList(self):
		if not self.cbWConnList:
			print('No connList CB')
			return


		portsA = self.cbWConnList()

		for port in portsA:
			self.layout.ddPorts.insertItem(0,port)



	def dispatchRun(self):
		if not self.cbWDispatch:
			print('No dispatch CB')
			return


		if not self.cbWDispatch(self.layout.ddPorts.currentText()):
			print("Device " + _dev + " disconnected")
