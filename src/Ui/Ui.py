#  todo 20 (module-ui, error) +0: handle errors, maybe status string
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer
#  todo 149 (module-ui, feature) +0: multiscene
#  todo 191 (filter, feature) +2: outline, fill and shape-intersect filters

# -todo 186 (feature, module-ui, module-dispatch, v2) +0: live cut visualize
#  todo 190 (feature, module-ui) +0: live cut visualize from standalone dispatcher, with some echo protocol
# =todo 117 (ux, module-ui) +0: add app settings
# =todo 184 (ux, module-ui) +0: save/load app settings with project

# =todo 178 (ux) +0: suggest recent at load

# =todo 175 (module-ui, module-data, geo) +0: clone geo
# =todo 176 (module-ui, module-data, geo) +0: del geo
# =todo 219 (module-ui, module-data, geo) +0: edit Geoblock transform

# =todo 169 (module-ui, ux, mark) +0: del mark
# -todo 170 (module-ui, ux, mark) +0: reorder mark
# =todo 171 (module-ui, ux, mark) +0: select by mark
# =todo 172 (module-ui, ux, mark) +0: unselect mark/close mark box
# -todo 173 (module-ui, ux, mark) +0: hover mark show toolbox

#  todo 208 (viewport) +0: viewport controls
# -todo 168 (module-ui, viewport, v2) +0: select by viewport

# =todo 165 (feature, dispatch) +0: device definition
# =todo 166 (module-ui, ux) +0: icons
#  todo 222 (feature) +2: independent undo/preset stack for any Geo and Mark

# =todo 179 (clean) -1: chack names, order and var/function annotates

import json


from .AppWindow import *
from .Utils import *



class Ui():
	defaultMarkData = {
		'Mark Color': '#777', #dummy
		'Laser Cycle': 100.
	}
	defaultMarkColorField = 'Mark Color'


	styleList = {
		'dark':'./Ui/schemes/default dark.qss',
		'light':'./Ui/schemes/default light.qss',
	}
	styleSVG = {
		'dark': {
			'default': {
				'vector-effect': 'non-scaling-stroke',
				'stroke-width':'2px',
				'stroke':'#99e',
				'fill':'#262640',
				'fill-opacity':'0.3',
				'opacity': '1'
			},
			'off': {
				'fill':'#282828',
				'stroke':'#444',
				'opacity': '.3',
				'fill-opacity':'0.1',
			},
			'select': {
				'fill':'#820',
				'stroke':'#f44',
			},
			'hover': {
				'stroke-width':'3px',
				'stroke':'#fe0',
				'opacity': '1',
			},
			'inactive': {
				'stroke-width':'1px',
				'stroke':'#777',
				'fill':'none',
			}
		},
		'light': {
			'default': {
				'vector-effect': 'non-scaling-stroke',
				'stroke-width':'2px',
				'fill':'#8cf',
				'stroke':'#48c',
				'fill-opacity':'0.3',
				'opacity': '1'
			},
			'off': {
				'fill':'#f8f8f8',
				'stroke':'#888',
				'opacity': '.3',
				'fill-opacity':'0.1',
			},
			'select': {
				'fill':'#fc8',
				'stroke':'#c80',
			},
			'hover': {
				'stroke-width':'3px',
				'stroke':'#f00',
				'opacity': '1'
			},
			'inactive': {
				'stroke-width':'1px',
				'stroke':'#777',
				'fill':'none',
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


# -todo 148 (module-ui, fix) +0: review scene life cycle
	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch


		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))


		self.appWindow = AppWindow(self.styleList[self.styleSet])

		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.sigPreexit.connect(self.preexit)

		self.appWindow.sigGeoSelect.connect(self.geoSetSelect)
		self.appWindow.sigGeoHover.connect(self.geoSetHover)
		self.appWindow.sigGeoDataSet.connect(self.geoSetData)
		self.appWindow.sigMarkAdd.connect(self.markCreate)
		self.appWindow.sigGeoActivate.connect(self.geoActivate)

		self.appWindow.sigSceneReset.connect(self.sceneReset)
		self.appWindow.sigSceneSave.connect(self.sceneSave)
		self.appWindow.sigSceneLoad.connect(self.sceneLoad)
		self.appWindow.sigAddFile.connect(self.addFile)

		self.appWindow.connList(self.dispatch.getDevices())
		self.appWindow.sigDispatch.connect(self.dispatchSend)
		self.appWindow.sigStoreG.connect(self.storeG)


		self.markDefault = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['default'],
			priority=-5,
		)
		self.markOff = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['off'],
			priority=-4,
#			data={'visible':False} #mark-level visibility for example
		)
		self.markSelect = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['select'],
			priority=-3,
		)
		self.markHover = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['hover'],
			priority=-2,
		)
		self.markInactive = self.data.markNew(
			filterName='FilterSetSVG',
			filterData=self.styleSVG[self.styleSet]['inactive'],
			priority=-1,
		)


		self.sceneCreate()



	def preexit(self, _e):
		if self.sceneDirty():
			_e.ignore()



	def exec(self):
		self.appWindow.show()


		self.qApp.exec_()


		self.args.set('wMaxi', self.appWindow.lMain.isMaximized())
		if not self.appWindow.lMain.isMaximized():
			cSize = self.appWindow.lMain.size()
			self.args.set('wSize', (cSize.width(), cSize.height()) )



### SLOTS ###


# =todo 188 (module-data, api) +0: move all data functions to data
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



	def sceneCreate(self, _name=''):
		self.activeScene = self.data.sceneGet(_name)
		self.appWindow.slotNewScene(self.activeScene)



	def sceneReset(self):
		if self.sceneDirty():
			return


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)


		self.sceneCreate()



	def sceneLoad(self):
		if self.sceneDirty():
			return


		cRecentA = self.args.get("recentProject", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(self.appWindow.lMain, "Open project", os.path.dirname(cLast), "*.codeg", None, QFileDialog.DontUseNativeDialog)[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentProject", cRecentA+[fileName])


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)


		with open(fileName, 'r') as f:
			projData = json.loads( f.read() )

		self.sceneCreate(projData['name'])


		marksA = {}
		for cMarkId in projData['markBlock']:
			markData = projData['markBlock'][cMarkId]
			cMark = marksA[int(cMarkId)] = self.data.markNew(data=markData['data'], filterName=markData['filter'], filterData={}, priority=markData['priority'])

			self.activeScene.markAppend(cMark)
			self.markAdd(cMark)


		for geoData in projData['geoBlock']:
#  todo 217 (module-data, ux) +0: detect missing geometry file
			cGBlock = self.activeScene.geoAdd(geoData['source'], [self.markDefault], name=('name' in geoData and geoData['name']))
# =todo 197 (data, fix) +0: deal with missing svg link
			for itemData in geoData['items']:
				cGItem = cGBlock.getGeo([itemData['name']])[0]


				for cMark in itemData['marks']:
					cGItem.markSet(marksA[cMark], True)


				cData = itemData['data']
				cGItem.dataSet(cData)
# -todo 183 (ux, module-ui) +1: brush Scene routines
				if ('visible' in cData) and (cData['visible'] == False):
					cGItem.markSet(self.markOff, [cGItem.name], True)

				cGItem.marksSolve(filterStep='UI')


			self.appWindow.geoAddWidget(cGBlock)


		self.appWindow.viewportFit()

		self.activeScene.clean()



# =todo 182 (ux) +0: fix save saved project
#  todo 196 (module-data, api) +0: deal with Markfilter data fields within Mark
# =todo 198 (data, fix) +0: move save/load routines to GGData
# =todo 203 (ux, clean) +0: scene load/save error handling
	def sceneSave(self):
		cRecentA = self.args.get("recentProject", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		
		cDialog = QFileDialog(self.appWindow.lMain, "Save project", os.path.dirname(cLast), "Codeg (*.codeg)")
		cDialog.setDefaultSuffix(".codeg")
		cDialog.setOptions(QFileDialog.DontUseNativeDialog)
		cDialog.setAcceptMode(QFileDialog.AcceptSave)
		if not cDialog.exec():
			return


		saveData = self.activeScene.packScene()

		fileName = cDialog.selectedFiles()[0]
		with open(fileName, 'w') as f:
			f.write( json.dumps(saveData, indent=2) )

		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentProject", cRecentA+[fileName])


		self.activeScene.clean()


# =todo 216 (module-data, clean) +0: use relative paths
#  todo 3 (feature, file) +0: geo library
	def addFile(self):
		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(self.appWindow.lMain, "Open SVG File", os.path.dirname(cLast), "*.svg", None, QFileDialog.DontUseNativeDialog)[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		cGBlock = self.activeScene.geoAdd(fileName, [self.markDefault], 'UI')
		self.appWindow.geoAddWidget(cGBlock)

		self.appWindow.viewportFit()



# -todo 119 (refactor, module-ui, module-data) +0: clean for dispatch
	def storeG(self):
		cRecentA = self.args.get("recentSaved", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''

		cDialog = QFileDialog(self.appWindow.lMain, "Save G-code", os.path.dirname(cLast), "G-code (*.nc)")
		cDialog.setDefaultSuffix(".nc")
		cDialog.setOptions(QFileDialog.DontUseNativeDialog)
		cDialog.setAcceptMode(QFileDialog.AcceptSave)
		if not cDialog.exec():
			return


		fileName = cDialog.selectedFiles()[0]

		h = self.appWindow.wSvgViewport.canvas.docHeight
		with open(fileName, 'w') as f:
			f.write(self.activeScene.getG(0, h))


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentSaved", cRecentA+[fileName])



# -todo 88 (fix, gcode) +0: use dispatch both for file save
	def dispatchSend(self, _name):
		return self.dispatch.runDevice(self.activeScene, _name, self.appWindow.dispatchLog)



### GEO ###


#  todo 98 (module-ui, optimize) -1: prevent doubling by difference change
	def geoSetSelect(self, _item, _state):
		_item.markSet(self.markSelect, _state,
			dirty=self.activeScene.markIn(self.markSelect))

		_item.marksSolve(filterStep='UI')



#  todo 77 (fix, module-ui, viewport, decide) -1: duplicate hover element topmost
	def geoSetHover(self, _item, _state):
		_item.markSet(self.markHover, _state,
			dirty=self.activeScene.markIn(self.markHover))

		_item.marksSolve(filterStep='UI')




	def geoSetData(self, _item, _names):
		if 'visible' not in _names:
			return

		_item.markSet(self.markOff, not _item.dataGet('visible', True),
			dirty=self.activeScene.markIn(self.markOff))

		_item.marksSolve(filterStep='UI')



	def geoActivate(self, _block, _state):
		for cGItem in _block.getGeo():
			cGItem.markSet(self.markInactive, not _state,
				dirty=self.activeScene.markIn(self.markInactive))

			cGItem.marksSolve(filterStep='UI')



### MARKS ###

# =todo 164 (feature, module-ui) -1: auto-apply new Mark to selection
	def markCreate(self):
		randomColor = QColor.fromHsvF(
			Counter.next('hue',.3)%1.,
			Counter.next('sat',.45)%1. *.5+.5,
			Counter.next('val',.15)%1. *.5+.5
		)

		cData = dict(self.defaultMarkData)
		cData[self.defaultMarkColorField] = randomColor.name()

		cMark = self.data.markNew( data=cData )
		self.activeScene.markAppend(cMark)


		self.appWindow.markAddWidget(cMark, True, colorName=self.defaultMarkColorField)



	def markAdd(self, _mark):
		self.appWindow.markAddWidget(_mark, colorName=self.defaultMarkColorField)
