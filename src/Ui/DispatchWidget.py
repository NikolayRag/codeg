from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


from .Tracer import *



class DispatchWidget(QObject):
	sigProgress = Signal(float)

	sigDevChange = Signal(object)
	sigDispatchFire = Signal(str)



	def dispatchFill(self, _devices, _default, add=False):
		oldList = {self.wListDevs.itemText(i):self.wListDevs.itemData(i) for i in range(self.wListDevs.count())}

		if add:
			_devices = set([_devices]) | set(oldList.keys())


		self.wListDevs.blockSignals(True)
		self.wListDevs.clear()
		self.wListDevs.blockSignals(False)


		if _default not in _devices:
			self.wListDevs.addItem(_default, False)
			self.wListDevs.setCurrentIndex(self.wListDevs.count()-1)


		for devName in _devices:
			self.wListDevs.addItem(devName, True)

			if devName == _default:
				self.wListDevs.setCurrentIndex(self.wListDevs.count()-1)



	def devChanged(self, i):
		_name = self.wListDevs.currentText()
		_enabled = self.wListDevs.currentData()

		self.args.last = _name

#  todo 257 (ux) +0: handle nonexistent device
		self.wBtnDispFire.setEnabled(_enabled)

		self.sigDevChange.emit(self.dispatch.devicePlate(_name))



	def __init__(self, _wRoot, _dispatch, _args, _viewport):
		QObject.__init__(self)

		self.dtStart = 0

		self.lenFeed = 0
		self.lenPoints = 0
		self.lenShapes = 0

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args
		
		self.tracer = Tracer(_viewport)


### setup ###

		self.wBtnRescan = _wRoot.findChild(QWidget, "btnRescan")
		self.wListDevs = _wRoot.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = _wRoot.findChild(QWidget, "btnDispFire")

# -todo 276 (ux, clean) +0: clean device rescan cycle
		self.wBtnRescan.clicked.connect(_dispatch.getDevices)
		self.wListDevs.currentIndexChanged.connect(self.devChanged)
		self.wBtnDispFire.clicked.connect(lambda: self.sigDispatchFire.emit(self.wListDevs.currentText()))

		_dispatch.sigDeviceListed.connect(lambda devA:self.dispatchFill(devA, self.args.last))
		_dispatch.sigDeviceFound.connect(lambda devA:self.dispatchFill(devA, self.args.last, add=True))


		self.wBtnTraceLive = _wRoot.findChild(QWidget, "btnTraceLive")
		self.wBtnTraceShapes = _wRoot.findChild(QWidget, "btnTraceShapes")

		self.wFrameDev = _wRoot.findChild(QWidget, "frameDev")
		self.wLabStats = _wRoot.findChild(QWidget, "labStats")

		_dispatch.sigDispatchAdded.connect(self.sessionPrepare)


		self.wBtnTraceLive.setChecked(self.args.visTracer)
		self.wBtnTraceShapes.setChecked(self.args.visTraceShapes)

		self.wBtnTraceLive.toggled.connect(lambda v: self.show(live=v))
		self.wBtnTraceShapes.toggled.connect(lambda v: self.show(shapes=v))


		self.show(self.args.visDispatch, live=self.args.visTracer, shapes=self.args.visTraceShapes)



	def show(self, _vis=None, live=None, shapes=None):
		if _vis!=None:
			self.args.visDispatch = _vis

		if live != None:
			self.wBtnTraceShapes.setEnabled(live)
			self.args.visTracer = live

		if shapes != None:
			self.args.visTraceShapes = shapes


		self.wRoot.setVisible(self.args.visDispatch)

		self.tracer.toggleVis(
			self.args.visDispatch and self.args.visTracer,
			self.args.visDispatch and self.args.visTracer and self.args.visTraceShapes
		)



	def sessionPrepare(self, _session):
		_session.sigStart.connect(lambda: self.traceReset(_session))
		_session.sigFeed.connect(lambda res, echo: self.traceFeed(_session, res, echo))
		_session.sigFinish.connect(lambda res: self.traceFinal(_session, res))



	def traceReset(self, _session=None):
		self.tracer.reset(_session and _session.viewBox())

		if _session:
			self.dtStart = datetime.now()

			self.lenFeed = 0
			self.lenPoints = 0
			self.lenShapes = 0

			self.wLabStats.setPlainText('')
			self.wFrameDev.appendPlainText(f"{str(self.dtStart)[:-5]}:\nDispatch begin")
			self.sigProgress.emit(0)



	def traceFeed(self, _session, _res, _echo):
		dt = datetime.now()-self.dtStart
#  todo 301 (trace) +0: show computed feed, points rate
#  todo 302 (trace) +0: show path kpi and segments metrics
		self.wLabStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		self.lenFeed += 1
		self.sigProgress.emit(self.lenFeed/_session.pathLen())


		edge = re.findall("S([\d]+)", _echo)
		if edge and float(edge[0])==0:
			self.lenShapes += 1
			self.tracer.split()


		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _echo)
		if coords:
			self.lenPoints += 1

			self.tracer.moveto((float(coords[0][0]), -float(coords[0][1])))


		if _res != True:
			self.tracer.spot(_res)

			self.wFrameDev.appendPlainText((f"{_res or 'Warning'}:\n ") + _echo)



	def traceFinal(self, _session, _res):
		self.tracer.final(_res)

		self.lenPoints -= 1 #last shape is park
		self.lenShapes -= 1
		
		dt = datetime.now()-self.dtStart
		self.wLabStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		self.wFrameDev.appendPlainText(f"{str(datetime.now())[:-5]}:\nDispatch {'end' if _res else 'error'}\nin {str(dt)[:-5]}\nwith {self.lenShapes}/{self.lenPoints} sh/pt\n")

#  todo 294 (Tracer, unsure) +0: check memory leak on subsequent sessions
		del _session
