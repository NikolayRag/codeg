#  todo 20 (module-ui, error) +0: handle errors, maybe status string
# -todo 23 (module-ui, ux) +0: show progress for time consuming operations
#  todo 27 (module-data, module-ui, ux) +0: allow append gcode from text buffer

# =todo 117 (ux, module-ui) +0: add app settings

from .AppWindow import *


class Ui():
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
				'stroke':'#444',
				'fill':'#fdfdfd',
				'opacity': '.9'
			},
			'off': {
				'fill':'#f8f8f8',
				'stroke':'#888',
				'opacity': '.3'
			},
			'select': {
				'fill':'#fe8',
				'stroke':'#861',
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



	def __init__(self, _args, _data, _dispatch):
		self.args = _args

		self.data = _data
		self.dispatch = _dispatch

		#init
		QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.qApp = QApplication()
		self.qApp.setStyle(QStyleFactory.create('fusion'))


		self.appWindow = AppWindow(self.defUi, self.styleList[self.styleSet])

		self.appWindow.sigResize.connect(self.storeWindow)
		self.appWindow.resize(
			self.args.get('wSize'),
			self.args.get('wMaxi')
		)


		self.appWindow.sigAddFile.connect(self.addFile)
		self.appWindow.sigStoreG.connect(self.storeG)
		self.appWindow.sigLayerSelect.connect(self.layerSetSelect)
		self.appWindow.sigLayerHover.connect(self.layerSetHover)
		self.appWindow.sigCtrlLayersSet.connect(self.ctrlLayersSet)

		self.appWindow.connList(self.dispatch.getDevices())
		self.appWindow.sigDispatch.connect(self.dispatchSend)


		self.markDefault = self.data.markNew(
			self.styleSVG[self.styleSet]['default'], -1)
		self.markOff = self.data.markNew(
			self.styleSVG[self.styleSet]['off'], 0)
		self.markSelect = self.data.markNew(
			self.styleSVG[self.styleSet]['select'], 1)
		self.markHover = self.data.markNew(
			self.styleSVG[self.styleSet]['hover'], 2)



	def exec(self):
		self.appWindow.show()


		self.qApp.exec_()



### PRIVATE ###



# -todo 88 (fix, gcode) +0: use dispatch both for file save
	def dispatchSend(self, _name):
		return self.dispatch.runDevice(_name, self.appWindow.dispatchLog)



#  todo 120 (refactor, module-ui, module-data) +0: clean, previous size
	def storeWindow(self, _size, _maximized):
		self.args.set('wMaxi', _maximized)
		if not _maximized:
			self.args.set('wSize', (_size.width(),_size.height()) )


# -todo 118 (refactor, module-ui, module-data) +0: clean for minor import
	def addFile(self):
		cRecentA = self.args.get("recentLoaded", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getOpenFileName(None, "Open SVG File", os.path.dirname(cLast), "*.svg")[0]

		if fileName=="":
			return

		
		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentLoaded", cRecentA+[fileName])


		self.data.newScene()
		cMeta = self.data.loadGeo(fileName, 'svg')
		self.data.markApply(self.markDefault, cMeta.keys(), at='UI')

		cXml = self.data.getXML()
		if cXml:
			self.appWindow.reactAddFile(cMeta, cXml)
		


# -todo 119 (refactor, module-ui, module-data) +0: clean for dispatch
	def storeG(self):
		if not self.data.available():
			print("No scene data")
			return


		cRecentA = self.args.get("recentSaved", [])

		cLast = cRecentA[len(cRecentA)-1] if len(cRecentA) else ''
		fileName = QFileDialog.getSaveFileName(None, "Save G", os.path.dirname(cLast), "*.nc")[0]

		
		if fileName=="":
			return


		h = self.appWindow.lViewport.canvas.docHeight
		with open(fileName, 'w') as f:
			f.write(self.data.getG(0, h))


		if cRecentA.count(fileName): cRecentA.remove(fileName)
		self.args.set("recentSaved", cRecentA+[fileName])



#  todo 98 (module-ui, optimize) -1: prevent doubling by difference change
	def layerSetSelect(self, _selectionA):
		self.data.markApply(self.markSelect, _selectionA, at='UI')

		self.reloadXml()



#  todo 77 (fix, module-ui, viewport) +0: duplicate hover element topmost
	def layerSetHover(self, _hover):
		self.data.markApply(self.markHover, [_hover] if _hover else [], at='UI')

		self.reloadXml()



	def ctrlLayersSet(self, _elA, _on):
		self.data.markApply(self.markOff, _elA, add=(not _on), at='UI')

		self.reloadXml()



	def reloadXml(self):
		cXml = self.data.getXML()
		if cXml:
			self.appWindow.canvasUpdate(cXml)
