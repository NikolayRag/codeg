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



class BindFilter(QObject):
	eType = None
	cb = None


	def __init__(self, _etypes, _cb):
		QObject.__init__(self)

		if not hasattr(_etypes, '__iter__'):
			_etypes = (_etypes,)
		self.eTypes = _etypes
		self.cb = _cb


	def eventFilter(self, _o, _e):
		if _e.type() in self.eTypes:
			self.cb(event=_e)

		return False



class AppWindow():
	aboutHref = "https://github.com/NikolayRag/codeg"

	cbWFileLoad = None
	cbWFileSave = None
	cbWConnList = None
	cbWDispatch = None
	cbWLayerSet = None


	qApp = None

	layout = Object()



	def setCBFileLoad(self, _cb):
		self.cbWFileLoad = _cb



	def setCBFileSave(self, _cb):
		self.cbWFileSave = _cb



	def setCBLayerSet(self, _cb):
		self.cbWLayerSet = _cb



	def setCBConnList(self, _cb):
		self.cbWConnList = _cb

		self.connList()



	def setCBDispatch(self, _cb):
		self.cbWDispatch = _cb



	def setCBResize(self, _cb):
		self.cbWResize = _cb



	def __init__(self):
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))
#  todo 50 (module-ui) +0: add style
#		with open('Ui/style.qss') as fQss:
#			self.qApp.setStyleSheet(fQss.read())

		selfPath= os.path.abspath(os.path.dirname(__file__))
		uiFile = os.path.join(selfPath,'AppWindow.ui')
		cMain = self.layout.main = QUiLoader().load(uiFile)

		cMain.setWindowTitle('codeg');
		self.tmpFilterWindowResize = BindFilter(
			(QEvent.Type.Resize, QEvent.Type.WindowStateChange),
			self.resized
		)
		cMain.installEventFilter(self.tmpFilterWindowResize)


		#widgets time
		self.layout.listLayers = cMain.findChild(QTableWidget, "listLayers")
		self.layout.listLayers.setEditTriggers(QAbstractItemView.NoEditTriggers);

		self.layout.listLayers.itemSelectionChanged.connect(self.layerSelect)
		self.layout.listLayers.cellEntered.connect(self.layerHover)
		self.tmpFilterLayersLeave = BindFilter(QEvent.Type.Leave, self.layerHover)
		self.layout.listLayers.installEventFilter(self.tmpFilterLayersLeave)


		holderViewport = cMain.findChild(QWidget, "wViewport")
# -todo 81 (module-ui, svg, feature) +0: show grid
		self.layout.viewport = SvgViewport(holderViewport)
		self.layout.viewport.lower()
		self.layout.viewport.show()

		self.tmpFilterViewResize = BindFilter(
			QEvent.Type.Resize,
			lambda event: self.layout.viewport.resize(event.size())
		)
		holderViewport.installEventFilter(self.tmpFilterViewResize)


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
		self.layout.logDev = cMain.findChild(QTextEdit, "logDev")


		self.layout.btnCaption.clicked.connect(self.about)
		self.layout.btnOpen.clicked.connect(self.openFile)
		self.layout.btnStore.clicked.connect(self.storeFile)
		self.layout.btnProccess.clicked.connect(self.dispatchRun)



	'''
	Display UI and enter QT app loop
	'''
	def exec(self):
		self.layout.main.show()


		self.qApp.exec_()



	def resize(self, _size, maximize=None):
		self.layout.main.resize(
			QSize(*_size)
			if _size else
			QApplication.primaryScreen().size() *.8
		)

		if maximize:
			self.layout.main.showMaximized()



#  todo 79 (module-ui, ux, fix) +0: make size ignored on maximize
	def resized(self, event):
		if not self.cbWResize:
			print('No resize CB')
			return

		wSize = self.layout.main.size()
		self.cbWResize(
			wSize,
			self.layout.main.isMaximized()
		)



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

			self.layout.viewport.canvasNew()
			self.layout.viewport.canvasAdd(cData['xml'])
			self.layout.viewport.canvasFit(.8)


			cList = self.layout.listLayers
			cList.setRowCount(0)
			cRow = 0

			for cItem in cData['meta']:
				cList.insertRow(cRow)
				cList.setItem(cRow, 0, QTableWidgetItem(cItem))
				cRow += 1

			#blank
			cList.insertRow(cRow)
			cItem = QTableWidgetItem()
			cItem.setFlags(Qt.NoItemFlags)
			cList.setItem(cRow, 0, cItem)


		


#  todo 20 (module-ui, error) +0: handle errors, maybe status string



	def storeFile(self):
		if not self.cbWFileSave:
			print('No save CB')
			return


		self.cbWFileSave()




	def layerSelect(self):
		if not self.cbWLayerSet:
			print('No layerSet CB')
			return


		selectionNamesA = []

		for cRange in self.layout.listLayers.selectedRanges():
			for cRow in range(cRange.topRow(), cRange.bottomRow()+1):
				if cRow < self.layout.listLayers.rowCount()-1:
					cName = self.layout.listLayers.item(cRow,0)

					selectionNamesA.append( cName.text() )


		cXml = self.cbWLayerSet(selection=selectionNamesA)
		if cXml:
			self.layout.viewport.canvasUpdate(cXml)



	def layerHover(self, _row=-1, _col=-1, event=None):
		if not self.cbWLayerSet:
			print('No layerSet CB')
			return


		hoverName = None
		if (_row > -1) and (_row < self.layout.listLayers.rowCount()-1):
			hoverName = self.layout.listLayers.item(_row,0).text()


		cXml = self.cbWLayerSet(hover=hoverName)
		if cXml:
			self.layout.viewport.canvasUpdate(cXml)



# -todo 59 (module-ui, ux, clean) +0: make updatable connections list
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


		self.cbWDispatch( self.layout.ddPorts.currentText() )



	def dispatchLog(self, _txt):
		self.layout.logDev.insertPlainText(_txt)
