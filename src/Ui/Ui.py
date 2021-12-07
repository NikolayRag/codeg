# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer
#  todo 149 (module-ui, feature) +0: multiscene
#  todo 191 (filter, feature) +2: outline, fill and shape-intersect filters

# -todo 184 (ux, module-ui) +0: save/load app settings with project

# =todo 178 (ux, feature) +0: suggest recent at load

# =todo 175 (module-ui, module-data, geo) +0: clone geo
# =todo 176 (module-ui, module-data, geo) +0: del geo
# =todo 219 (module-ui, module-data, geo) +0: edit Geoblock transform

# =todo 169 (module-ui, ux, mark) +0: del mark
# -todo 170 (module-ui, ux, mark) +0: reorder mark
# =todo 171 (module-ui, ux, mark) +0: select by mark
# =todo 172 (module-ui, ux, mark) +0: unselect mark/close mark box
# -todo 173 (module-ui, ux, mark) +0: hover mark show toolbox

#  todo 208 (viewport) +0: viewport controls

# =todo 166 (module-ui, ux) +0: icons
#  todo 222 (feature) +2: independent undo/preset stack for any Geo and Mark

# =todo 179 (clean) -1: check names, order and var/function annotates

import json


from .DispatchLink import *
from .AppWindow import *
from .Utils import *
from Args import *



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
				'stroke-width':'2.5px',
				'stroke':'#99e',
				'fill':'#262640',
				'fill-opacity':'0.3',
				'opacity': '1'
			},
			'inactive': {
				'stroke-width':'1px',
				'stroke':'#ddd',
				'fill':'none',
			},
			'off': {
				'fill':'#282828',
				'stroke':'#444',
				'opacity': '.5',
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
		},
		'light': {
			'default': {
				'vector-effect': 'non-scaling-stroke',
				'stroke-width':'2.5px',
				'fill':'#8cf',
				'stroke':'#48c',
				'fill-opacity':'0.3',
				'opacity': '1'
			},
			'inactive': {
				'stroke-width':'1px',
				'stroke':'#444',
				'fill':'none',
			},
			'off': {
				'fill':'#f8f8f8',
				'stroke':'#888',
				'opacity': '.5',
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
		}
	}



	# statics
	qApp = None
	appWindow = None
	data = None
	dispatch = None


	# runtime

	activeScene = None
	activeDevice = None


	def __init__(self, _data, _dispatch):


		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))


		self.data = _data

		self.dispatch = _dispatch

		self.appWindow = AppWindow(self.dispatch)


		self.appWindow.sigPrefScheme.connect(self.prefScheme)
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
		self.appWindow.sigPaste.connect(self.paste)

#  todo 276 (ux, clean) +0: clean device rescan cycle
		self.appWindow.sigDevChange.connect(self.dispatchChanged)
		self.appWindow.sigDispatchFire.connect(self.dispatchSend)
		self.appWindow.sigDispatchShot.connect(self.dispatchShot)

		#default device as template, overrided at actual dispatch
		self.appWindow.dispatchFill({}, Args.Dispatch.last)
		_dispatch.getDevices()


		self.markDefault = self.data.markNew(
			filterName='FilterSetSVG',
			priority=-5,
		)
		self.markInactive = self.data.markNew(
			filterName='FilterSetSVG',
			priority=-4,
		)
		self.markOff = self.data.markNew(
			filterName='FilterSetSVG',
			priority=-3,
#			data={'visible':False} #mark-level visibility for example
		)
		self.markSelect = self.data.markNew(
			filterName='FilterSetSVG',
			priority=-2,
		)
		self.markHover = self.data.markNew(
			filterName='FilterSetSVG',
			priority=-1,
		)


		self.prefScheme()


		self.sceneCreate()



# -todo 248 (ux, feature) +0: update default plate size
	def prefScheme(self):
		self.appWindow.setStyle(self.styleList[Args.Application.scheme])


		self.markDefault.setData(self.styleSVG[Args.Application.scheme]['default'])
		self.markInactive.setData(self.styleSVG[Args.Application.scheme]['inactive'])
		self.markOff.setData(self.styleSVG[Args.Application.scheme]['off'])
		self.markSelect.setData(self.styleSVG[Args.Application.scheme]['select'])
		self.markHover.setData(self.styleSVG[Args.Application.scheme]['hover'])

		if self.activeScene:
			for geoBlock in self.activeScene.geoList():
				for geoItem in geoBlock.getGeo():
					geoItem.marksSolve(filterStep='UI', force=True)

		self.appWindow.geoWidgetTouched()



	def preexit(self, _e):
		if self.sceneDirty():
			_e.ignore()



	def exec(self):
		cPos = Args.Application.wPos and QPoint(*Args.Application.wPos)
		cMargin = QApplication.primaryScreen().size() *(1-Args.Application.initFit)
		cPos = cPos or QPoint(cMargin.width(), cMargin.height())

		cSize = Args.Application.wSize and QSize(*Args.Application.wSize)
		cSize = cSize or QApplication.primaryScreen().size() *Args.Application.initFit
		self.appWindow.windowGeometrySet(cSize, cPos, Args.Application.wMaxi)


		self.appWindow.show()
		self.qApp.exec_()


		wSize = self.appWindow.windowGeometry()
		Args.Application.wSize = (wSize[0].width(), wSize[0].height())
		Args.Application.wPos = (wSize[1].x(), wSize[1].y())
		Args.Application.wMaxi = wSize[2]



	def alert(self, _head, _msg):
		msgBox = QMessageBox()
		msgBox.setText(_head)
		msgBox.setInformativeText(_msg)
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec()



### SLOTS ###


	def sceneDirty(self):
		scenesList = self.data.sceneList()
		
		for cScene in scenesList:
			if scenesList[cScene].isDirty():
				msgBox = QMessageBox()
				msgBox.setText("Scene modified")
				msgBox.setInformativeText("Discard?")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				msgBox.setDefaultButton(QMessageBox.Cancel)
				if msgBox.exec() == QMessageBox.Cancel:
					return True



	def sceneCreate(self, _name=''):
		self.activeScene = self.data.sceneGet(_name)
		self.appWindow.slotNewScene(self.activeScene)

		self.appWindow.gridSize(self.dispatch.devicePlate(self.activeDevice))
		self.appWindow.viewportFit()


	def sceneReset(self):
		if self.sceneDirty():
			return


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)


		self.sceneCreate()



	def sceneLoad(self, _parent):
		if self.sceneDirty():
			return


		cRecentA = Args.Ui.recentProject

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(_parent, "Open project", os.path.dirname(cLast), "*.codeg", None, QFileDialog.DontUseNativeDialog)[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		Args.Ui.recentProject = cRecentA+[fileName]


		for cScene in self.data.sceneList():
			self.data.sceneRemove(cScene)


		with open(fileName, 'r') as f:
			projData = json.loads( f.read() )

		self.sceneCreate(projData['name'])


		self.appWindow.suspend(True)

		marksA = {}
		for cMarkId in projData['markBlock']:
			markData = projData['markBlock'][cMarkId]
			cMark = marksA[int(cMarkId)] = self.data.markNew(data=markData['data'], filterName=markData['filter'], filterData={}, priority=markData['priority'])

			self.activeScene.markAppend(cMark)
			self.markAdd(cMark)


		for geoData in projData['geoBlock']:
#  todo 217 (module-data, ux) +0: detect missing geometry file
			cGBlock = self.activeScene.geoAdd(geoData['source'], [self.markDefault], name=('name' in geoData and geoData['name']))
			cGBlock.xformSet(geoData['xform'])

# =todo 197 (data, fix) +0: deal with missing svg link
			for itemData in geoData['items']:
				cGItem = cGBlock.getGeo([itemData['name']])[0]


				for cMark in itemData['marks']:
					cGItem.markSet(marksA[cMark], True)


				cData = itemData['data']
				cGItem.dataSet(cData)
# -todo 183 (ux, module-ui) +1: brush Scene routines
				if ('visible' in cData) and (cData['visible'] == False):
					cGItem.markSet(self.markOff, True)

				if ('selected' in cData) and cData['selected']:
					cGItem.markSet(self.markSelect, True)


				cGItem.marksSolve(filterStep='UI')


			self.appWindow.geoAddWidget(cGBlock)

#  todo 225 (ux) +0: store viewport position/size within scene
		self.appWindow.viewportFit()

		self.activeScene.clean()


		self.appWindow.suspend(False)



# =todo 182 (ux) +0: save saved project with increment
#  todo 196 (module-data, API) +0: deal with Markfilter data fields within Mark
# -todo 198 (data, fix) +0: move save/load routines to GGData
# =todo 203 (ux, clean) +0: scene load/save error handling
	def sceneSave(self, _parent):
		cRecentA = Args.Ui.recentProject

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''

		cDialog = QFileDialog(_parent, "Save project", os.path.dirname(cLast), "Codeg (*.codeg)")
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
		Args.Ui.recentProject = cRecentA+[fileName]


		self.activeScene.clean()


# =todo 216 (module-data, clean) +0: use relative paths
#  todo 3 (feature, file) +0: geo library
	def addFile(self, _parent):
		cRecentA = Args.Ui.recentLoaded

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(_parent, "Open SVG File", os.path.dirname(cLast), "*.svg", None, QFileDialog.DontUseNativeDialog)[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		Args.Ui.recentLoaded = cRecentA+[fileName]


		cGBlock = self.activeScene.geoAdd(fileName, [self.markDefault], 'UI')
		cOffset = QPointF(*self.dispatch.devicePlate(self.activeDevice))
		cGBlock.xformSet(offset=(0,-cOffset.y()))
		gDscr = self.appWindow.geoAddWidget(cGBlock)

		self.appWindow.viewportFit(gDscr.bbox(), Args.Viewport.fitGeo)



	def paste(self):
		clipboard = QGuiApplication.clipboard()

		cGBlock = self.activeScene.geoAdd(clipboard.text(), [self.markDefault], 'UI', name='paste', raw=True)
		cOffset = QPointF(*self.dispatch.devicePlate(self.activeDevice))
		cGBlock.xformSet(offset=(0,-cOffset.y()))
		gDscr = self.appWindow.geoAddWidget(cGBlock)

		self.appWindow.viewportFit(gDscr.bbox(), Args.Viewport.fitGeo)



### DISPATCH ###


	def dispatchChanged(self, _name, _enabled):
		self.activeDevice = _name
		if self.activeScene:
			self.appWindow.gridSize(self.dispatch.devicePlate(self.activeDevice))



# -todo 119 (refactor, module-ui, module-data) +0: clean for dispatch
# todo 88 (fix, gcode, unsure) +0: use dispatch both for file save
	def dispatchShot(self, _parent):
		cRecentA = Args.Ui.recentSaved

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''

		cDialog = QFileDialog(_parent, "Save G-code", os.path.dirname(cLast), "G-code (*.nc)")
		cDialog.setDefaultSuffix(".nc")
		cDialog.setOptions(QFileDialog.DontUseNativeDialog)
		cDialog.setAcceptMode(QFileDialog.AcceptSave)
		if not cDialog.exec():
			return


		fileName = cDialog.selectedFiles()[0]

		with open(fileName, 'w') as f:
			f.write("\n".join(self.activeScene.traceG()['data']))


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		Args.Ui.recentSaved = cRecentA+[fileName]



#  todo 251 (module-dispatch, feature) +0: make generation by iterator
# -todo 264 (module-ui, module-dispatch, fix) +0: use actual box

	def dispatchSend(self, _name):
		self.dispatch.sessionStart(_name, self.activeScene.traceG())



### GEO ###


#  todo 98 (module-ui, optimize) -1: prevent doubling by difference change
	def geoSetSelect(self, _item, _state):
		_item.dataSet({'selected': _state})

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
			cSel = _state and cGItem.dataGet('selected', False)
			cGItem.markSet(self.markSelect, cSel,
				dirty=self.activeScene.markIn(self.markSelect))

			cGItem.markSet(self.markInactive, not _state,
				dirty=self.activeScene.markIn(self.markInactive))

			cGItem.marksSolve(filterStep='UI')



### MARKS ###

# -todo 164 (feature, module-ui, unsure) -1: auto-apply new Mark to selection
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
