#  todo 20 (module-ui, error) +0: handle errors, maybe status string
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer
#  todo 149 (module-ui, feature) +0: multiscene

# =todo 117 (ux, module-ui) +0: add app settings

from .AppWindow import *
from .Utils import *



class Ui():
	defaultMarkData = {
		'Mark Color': QColor('#777'),
		'Laser Cycle': 100.
	}
	defaultMarkColorField = 'Mark Color'


	defUi = './Ui/AppWindow.ui'

	styleList = {
		'dark':'./Ui/schemes/default dark.qss',
		'light':'./Ui/schemes/default light.qss',
	}
	styleSVG = {
		'dark': {
			'default': {
				'vector-effect': 'non-scaling-stroke',
				'stroke-width':'1.5px',
				'stroke':'#888',
				'fill':'#181818',
				'opacity': '.9'
			},
			'off': {
				'fill':'#282828',
				'stroke':'#444',
				'opacity': '.3'
			},
			'select': {
				'fill':'#820',
				'stroke':'#f44',
			},
			'hover': {
				'stroke-width':'2.5px',
				'stroke':'#fe0',
				'opacity': '.9'
			}
		},
		'light': {
			'default': {
				'vector-effect': 'non-scaling-stroke',
				'stroke-width':'1.5px',
				'stroke':'#666',
				'fill':'#fdfdfd',
				'opacity': '.9'
			},
			'off': {
				'fill':'#f8f8f8',
				'stroke':'#888',
				'opacity': '.3'
			},
			'select': {
				'fill':'#8cf',
				'stroke':'#04f',
			},
			'hover': {
				'stroke-width':'2.5px',
				'stroke':'#f00',
				'opacity': '.9'
			}
		}
	}
#  todo 115 (ux) -1: allow to choose style by commandline
# =todo 116 (ux, module-ui) +0: choose style in app settings
	styleSet = 'dark'


	args = None

	appWindow = None

	data = None
	qApp = None

	activeScene = None


# =todo 148 (module-ui, fix) +0: review scene life cycle
	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch


		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))


		self.appWindow = AppWindow(self.defUi, self.styleList[self.styleSet])

		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.sigSceneWipe.connect(self.sceneWipe)
		self.appWindow.sigAddFile.connect(self.addFile)
		self.appWindow.sigStoreG.connect(self.storeG)
		self.appWindow.sigLayerSelect.connect(self.layerSetSelect)
		self.appWindow.sigLayerHover.connect(self.layerSetHover)
		self.appWindow.sigCtrlLayersSet.connect(self.ctrlLayersSet)
		self.appWindow.sigMarkAdd.connect(self.slotMarkAdd)
		self.appWindow.sigMarkAssign.connect(self.slotMarkAssign)

		self.appWindow.connList(self.dispatch.getDevices())
		self.appWindow.sigDispatch.connect(self.dispatchSend)


		self.markDefault = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['default'],
			priority=-4,
		)
		self.markOff = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['off'],
			priority=-3,
#			data={'visible':False} #mark-level visibility for example
		)
		self.markSelect = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['select'],
			priority=-2,
		)
		self.markHover = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['hover'],
			priority=-1,
		)


		self.sceneNew()



	def exec(self):
		self.appWindow.show()


		self.qApp.exec_()

		
		self.args.set('wMaxi', self.appWindow.lMain.isMaximized())
		if not self.appWindow.lMain.isMaximized():
			cSize = self.appWindow.lMain.size()
			self.args.set('wSize', (cSize.width(), cSize.height()) )



### PRIVATE ###



# -todo 88 (fix, gcode) +0: use dispatch both for file save
	def dispatchSend(self, _name):
		return self.dispatch.runDevice(self.activeScene, _name, self.appWindow.dispatchLog)



	def sceneDirty(self):
		scenesList = self.data.sceneList()
		
		for cScene in scenesList:
			if scenesList[cScene].isDirty():
				msgBox = QMessageBox()
				msgBox.setText("Scene modified")
				msgBox.setInformativeText("Discard?")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				msgBox.setDefaultButton(QMessageBox.Ok)
				if msgBox.exec() == QMessageBox.Cancel:
					return True



	def sceneNew(self, _name=''):
		self.activeScene = self.data.sceneGet(_name)
		self.appWindow.slotNewScene(self.activeScene)



	def sceneWipe(self, _new=True):
		if self.sceneDirty():
			return


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)


		if _new:
			self.sceneNew()



#  todo 118 (refactor, module-ui, module-data) +0: clean for minor import
	def addFile(self):
		if self.sceneDirty():
			return


		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)

		self.sceneNew(fileName)

		self.activeScene.geoAdd(fileName, 'svg')
		self.activeScene.clean()
		
		cMeta = self.activeScene.geoMeta()
		self.activeScene.markApplyGeo(self.markDefault, cMeta.keys(), step='UI')

		cXml = self.activeScene.getSceneXML(True)
		if cXml:
			self.appWindow.reactAddFile(cMeta, cXml)
		


# -todo 119 (refactor, module-ui, module-data) +0: clean for dispatch
	def storeG(self):
		cRecentA = self.args.get("recentSaved", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(None, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		h = self.appWindow.lViewport.canvas.docHeight
		with open(fileName, 'w') as f:
			f.write(self.data.getG(self.activeScene, 0, h))


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentSaved", cRecentA+[fileName])



### LAYERS ###


#  todo 98 (module-ui, optimize) -1: prevent doubling by difference change
	def layerSetSelect(self, _selectionA):
		marksUsed = {}
		cObjA = self.activeScene.getSceneObjs(_selectionA)

		for cObj in cObjA:
			for cMark in cObj.marks:
				marksUsed[cMark] = True

		for cMark in marksUsed:
			for cObj in cObjA:
				if cMark not in cObj.marks:
					marksUsed[cMark] = False

		self.appWindow.marksSelect(marksUsed)


		self.activeScene.markApplyGeo(self.markSelect, _selectionA, step='UI')

		self.reloadXml()



#  todo 77 (fix, module-ui, viewport, decide) -1: duplicate hover element topmost
	def layerSetHover(self, _hover):
		self.activeScene.markApplyGeo(self.markHover, [_hover] if _hover else [], step='UI')

		self.reloadXml()



	def ctrlLayersSet(self, _elA, _on):
		self.activeScene.markApplyGeo(self.markOff, _elA, mode=(not _on), step='UI')
		self.activeScene.geoDataSet(_elA, {'visible':_on})

		self.reloadXml()



	def reloadXml(self):
		cXml = self.activeScene.getSceneXML(True)
		if cXml:
			self.appWindow.canvasUpdate(cXml)



### ITS MARK TIME ###


	def slotMarkAdd(self):
		cData = dict(self.defaultMarkData)
		cData[self.defaultMarkColorField] = QColor.fromHsvF(
			Counter.next('hue',.3)%1.,
			Counter.next('sat',.45)%1. *.5+.5,
			Counter.next('val',.15)%1. *.5+.5
		)

		cMark = self.data.markNew( data=cData )
		self.activeScene.markAppend(cMark)


		self.uiMarkAdd(cMark, True)



	def uiMarkAdd(self, _mark, _open=False):
		self.appWindow.wMarkAdd(_mark, _open, fieldColor=self.defaultMarkColorField)



	def slotMarkAssign(self, _mark, _geoList, _state):
		self.activeScene.markApplyGeo(_mark, list(_geoList.values()), mode=bool(_state), step='DIRECT')

		self.uiMarkAssign(_mark, list(_geoList.keys()), _state)



	def uiMarkAssign(self, _mark, _geoList, _state):
		self.appWindow.wMarkAssign(_mark, _geoList, _state)
