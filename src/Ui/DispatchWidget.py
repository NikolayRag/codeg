from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


from .Tracer import *



class DispatchWidget(QObject):
	sigProgress = Signal(float)

	sigDevChange = Signal(object)
	sigDispatchFire = Signal(str)



	def dispatchFill(self, _devices, _default, add=False):
		cList = {}

		if add:
			cList = {self.wListDevs.itemText(i):self.wListDevs.itemData(i) for i in range(self.wListDevs.count())}
			_devices = [_devices]

		if _default not in cList:
			cList[_default] = False

		for dev in _devices:
			cList[dev] = True


		self.wListDevs.blockSignals(True)
		self.wListDevs.clear()
		self.wListDevs.blockSignals(False)


		for dName, dState in cList.items():
			self.wListDevs.addItem(dName, dState)

			if dName == _default:
				self.wListDevs.setCurrentIndex(self.wListDevs.count()-1)



	def devChanged(self, i=-1):
		_name = self.wListDevs.currentText()
		_enabled = self.wListDevs.currentData()

		self.args.last = _name

		self.relock()

		self.sigDevChange.emit(self.dispatch.devicePlate(_name))




	def relock(self):
		_enabled = self.wListDevs.currentData()

		self.wBtnDispFire.setEnabled(_enabled and not self.session)
		self.wBtnDispPause.setEnabled(bool(self.session))
		self.wBtnDispCancel.setEnabled(bool(self.session))



	def log(self, _v):
		new_format = "%H:%M:%S"
		now = datetime.now().strftime(new_format)

		self.wFrameDev.appendPlainText(f"{now}: {_v}")



#  todo 308 (module-dispatch) +0: confirm pause/cancel
	def sessionCancel(self):
		self.session and self.session.cancel()



	def sessionPause(self, _state):
		self.session and self.session.pause(_state)



	def __init__(self, _wRoot, _dispatch, _args, _viewport):
		QObject.__init__(self)

		self.dtStart = 0

		self.lenFeed = 0
		self.lenPoints = 0
		self.lenShapes = 0

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args
		
		self.session = None
		self.tracer = Tracer(_viewport)


### setup ###

		self.wProgDispatch = _wRoot.findChild(QWidget, "progDispatch")

		self.wBtnRescan = _wRoot.findChild(QWidget, "btnRescan")
		self.wListDevs = _wRoot.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = _wRoot.findChild(QWidget, "btnDispFire")
		self.wBtnDispPause = _wRoot.findChild(QWidget, "btnDispPause")
		self.wBtnDispCancel = _wRoot.findChild(QWidget, "btnDispCancel")

# -todo 276 (ux, clean) +0: clean device rescan cycle
		self.wBtnRescan.clicked.connect(_dispatch.getDevices)
		self.wListDevs.currentIndexChanged.connect(self.devChanged)
		self.wBtnDispCancel.clicked.connect(self.sessionCancel)
		self.wBtnDispPause.toggled.connect(self.sessionPause)
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
		_session.sigFeed.connect(lambda res, echo, feed: self.traceFeed(_session, res, echo, feed))
		_session.sigFinish.connect(lambda res: self.traceFinal(_session, res))



	def traceReset(self, _session=None):
#  todo 305 (trace, v2) +0: move all session related trace runtime data to session
		self.tracer.reset(_session and _session.viewBox())

		if _session:
			self.session = _session
			self.relock()

			self.dtStart = datetime.now()

			self.lenFeed = 0
			self.lenPoints = 0
			self.lenShapes = 0

			self.wLabStats.setPlainText('')
			self.log("begin")
			self.wProgDispatch.setValue(0)
			self.sigProgress.emit(0)



	def traceFeed(self, _session, _res, _echo, _feed):
#  todo 301 (trace) +0: show computed feed, points rate
#  todo 302 (trace) +0: show path kpi and segments metrics
		dt = datetime.now()-self.dtStart
		self.wLabStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		self.lenFeed += 1
		prog = self.lenFeed/_session.pathLen()
		self.sigProgress.emit(prog)
		self.wProgDispatch.setValue(100*prog)


		edge = re.findall("S([\d]+)", _feed)
		if edge and float(edge[0])==0:
			self.lenShapes += 1
			self.tracer.split()


		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _feed)
		if coords:
			self.lenPoints += 1

			self.tracer.moveto((float(coords[0][0]), -float(coords[0][1])))


		if _res!=True:
			self.tracer.spot(True)

			self.log(f"{_res} at:\n{_feed}" + (("\n"+', '.join(_echo)) if _echo else ''))



	def traceFinal(self, _session, _res):
		self.lenPoints -= 1 #last shape is park
		self.lenShapes -= 1
		
		dt = datetime.now()-self.dtStart
		self.wLabStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		msgA = {_session.errOk:'end', _session.errDevice:'error'}
		self.log((msgA[_res] if _res in msgA else "unknown") +"\n")

#  todo 294 (Tracer, unsure) +0: check memory leak on subsequent sessions
		self.session = None
		del _session

		self.relock()
