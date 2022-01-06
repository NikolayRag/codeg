from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


import re
from datetime import datetime
import math


# =todo 336 (dispatch, device, feature) +0: make manual live CNC guide
#  todo 322 (dispatch, ui, v2) +0: rework dispatch/device/session widget entirely

class DispatchWidget(QObject):
	sigProgress = Signal(float)

	sigDevChange = Signal(object)
	sigDispatchFire = Signal(str)

	sigLive = Signal(bool)
	sigInteract = Signal(object, list)

	recoverSession = None


# -todo 276 (ux, clean) +0: clean device rescan cycle
	def dispatchFill(self, _devices, _default):
		cList = {self.wListDevs.itemText(i):self.wListDevs.itemData(i) for i in range(self.wListDevs.count())}

		if not _devices:
			cList = {}

		if _default not in cList:
			cList[_default] = False

		if _devices:
			cList[_devices] = True


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

		cState = self.dispatch.deviceState(_name)
		if cState[0] != None:
			msgErr = 'Connection dropped' if cState[0]<0 else f'Error {cState[0]}'
			self.devStateBlockState(cState[0]==True, msgErr)

		self.sigDevChange.emit(self.dispatch.devicePlate(_name))




#  todo 338 (module-dispatch, clean) +0: make dispatch ui modes
	def relock(self):
		_enabled = self.wListDevs.currentData()

		self.wBtnDispFire.setEnabled(_enabled and not self.activeSession)
		self.wBtnDispPause.setEnabled(bool(self.activeSession))
		self.wBtnDispCancel.setEnabled(bool(self.activeSession))
		self.wBtnDispStop.setEnabled(bool(self.activeSession and self.activeSession.pause()))

		self.wFrameRecover.setEnabled(_enabled and not self.activeSession)



	def logDispatch(self, _v):
		new_format = "%H:%M:%S"
		now = datetime.now().strftime(new_format)

		self.wFrameDev.appendPlainText(f"{now}: {_v}")



#  todo 313 (module-dispatch, v2) +0: review dispatch session stats
	def logSession(self, _sessionLive, _endMsg=''):
#		partCoords = f"X{_sessionLive.coords[0]} Y{_sessionLive.coords[1]}"

		dt = datetime.now()-_sessionLive.logTimeStart

		now = _sessionLive.logTimeStart.strftime("%H:%M:%S")

		partTime = f"{str(dt)[:-5]}"

		if _endMsg != '':
			_endMsg = f'finish: {_endMsg}'

#		partLeft = f"\n{int(dt.seconds / progress - dt.seconds)} sec left"
#		partLeft = partLeft if _sessionLive.logShapes>2 else ''
		self.wLabStats.setPlainText(f"start: {now}\ntime: {partTime}\nshapes: {_sessionLive.logShapes}\npoints: {_sessionLive.logPoints}\n{_endMsg}")



# -todo 308 (module-dispatch) +5: confirm stop
	def sessionCancel(self, _instant=False):
		if not self.activeSession:
			return
		
		self.wBtnDispPause.setChecked(False)

		self.activeSession.cancel(_instant)



	def sessionPause(self, _state):
		self.activeSession and self.activeSession.pause(_state)

		self.relock()



	def devStateBlockVis(self, _vis):
		self.args.visDevState = _vis



# -todo 325 (dispatch, clean) +0: display verbose device state
	def devStateBlockState(self, state, _msgErr=''):
		self.wBtnDevState.setObjectName('btnDevState' if state else 'btnDevState-warning')
		self.wBtnDevState.setStyleSheet(self.wBtnDevState.styleSheet())

		self.wLabRecover.setObjectName('labRecover' if state else 'labRecover-warning')
		self.wLabRecover.setStyleSheet(self.wBtnDevState.styleSheet())
		self.wLabRecover.setText('Normal state' if state else _msgErr)
			


	def devRecoverSelect(self, _i):
		self.args.devRecoverOption = _i



	def recoverStop(self, force=False):
			self.sigInteract.emit(False, [])

			if self.recoverSession:
				if force:
					self.recoverSession.cancel(True)

				self.recoverSession.final()

				self.recoverSession = None



	def recoverInteract(self, _offset, _live):
		_offset = (
			self.recoverGuideCoords[0] +_offset.x(),
			self.recoverGuideCoords[1] +_offset.y()
		)

		self.recoverSession.add([f'G90 X{_offset[0]}Y{-_offset[1]}'])

		self.recoverGuideCoords = _offset



#  todo 342 (guide, fix) +0: catch device errors while Guide
	def recoverRun(self):
		def recoverEnd(_session, res):
			self.devStateBlockState(res==1, f'Error while recover: {_session.resultRuntime[-1][0]}')

			self.wBtnDispFire.setEnabled(True)
			self.wBtnRecoverRun.setVisible(True)
			self.wBtnRecoverRun.setEnabled(True)
			self.wBtnRecoverStop.setVisible(False)

		
		self.devStateBlockState(True)

		self.wBtnDispFire.setEnabled(False)
		self.wBtnRecoverRun.setEnabled(False)

		cSession = self.recoverSession = (
			self.dispatch.sessionStart(self.wListDevs.currentText(), (0,1,0,1), [''], gIn=[''], gOut=[''], live=True)
		)
		cSession.sigFinish.connect(lambda res: recoverEnd(cSession, res))


		cOption = self.wListRecoverOpions.currentIndex()

		if cOption == 0:
			cSession.add(['$X'])
			cSession.final()

		if cOption == 1:
			cSession.add(['$H'])
			cSession.final()

		if cOption == 2:
#  todo 346 (device, guide, fix) +0: init Guide speed
			self.recoverSession.add(['$X'])

			self.wBtnRecoverRun.setVisible(False)
			self.wBtnRecoverStop.setVisible(True)

			cDeg = math.radians(float(self.wRecDeg.text()))
			cAmt = float(self.wRecAmt.text())

#  todo 333 (device, fix) +0: fix lost coords predict with jog
#			self.recoverGuideCoords = (math.cos(cDeg)*cAmt, -1*math.sin(cDeg)*cAmt)
			self.recoverGuideCoords = (0,0)
			self.sigInteract.emit(self.recoverInteract, self.recoverGuideCoords)


		cSession.start()
		



	def __init__(self, _wRoot, _dispatch, _args, _tracer):
		QObject.__init__(self)

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args
		
		self.activeSession = None
		self.tracer = _tracer


### setup ###

		self.wProgDispatch = _wRoot.findChild(QWidget, "progDispatch")

		self.wBtnRescan = _wRoot.findChild(QWidget, "btnRescan")
		self.wListDevs = _wRoot.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = _wRoot.findChild(QWidget, "btnDispFire")
		self.wBtnDispPause = _wRoot.findChild(QWidget, "btnDispPause")
		self.wBtnDispCancel = _wRoot.findChild(QWidget, "btnDispCancel")
		self.wBtnDispStop = _wRoot.findChild(QWidget, "btnDispStop")


		self.wBtnRescan.clicked.connect(_dispatch.getDevices)
		self.wListDevs.currentIndexChanged.connect(self.devChanged)
# =todo 344 (guide) +0: move force stop from Session to Device control
		self.wBtnDispCancel.clicked.connect(lambda: self.sessionCancel(True))
		self.wBtnDispPause.toggled.connect(self.sessionPause)
		self.wBtnDispFire.clicked.connect(lambda: self.sigDispatchFire.emit(self.wListDevs.currentText()))
		self.wBtnDispStop.clicked.connect(lambda: self.sessionCancel(False))

		self.wBtnTraceLive = _wRoot.findChild(QWidget, "btnTraceLive")
		self.wBtnTraceShapes = _wRoot.findChild(QWidget, "btnTraceShapes")


# -todo 332 (device, recover, feature) +0: add homing at start option
		self.wFrameRecover = _wRoot.findChild(QWidget, "frameRecover")
		self.wLabRecover = _wRoot.findChild(QWidget, "labRecover")
		self.wListRecoverCoords = _wRoot.findChild(QWidget, "lineRecoverCoords")
		self.wListRecoverOpions = _wRoot.findChild(QWidget, "listRecoverOpions")
		self.wListRecoverOpions.setCurrentIndex(self.args.devRecoverOption)
		self.wListRecoverOpions.currentIndexChanged.connect(self.devRecoverSelect)

		self.wFrameDevice = _wRoot.findChild(QWidget, "frameDevice")
		self.wBtnDevState = _wRoot.findChild(QWidget, "btnDevState")
		self.wBtnDevState.setChecked(self.args.visDevState)
		self.devStateBlockVis(self.args.visDevState)
		self.wBtnDevState.toggled.connect(self.devStateBlockVis)

		self.wRecDeg = _wRoot.findChild(QWidget, "lineRecDeg")
		self.wRecDeg.setValidator(QDoubleValidator())
		self.wRecAmt = _wRoot.findChild(QWidget, "lineRecAmt")
		self.wRecAmt.setValidator(QDoubleValidator())
#  todo 347 (device, ui, ux) +0: recover by vaues
		self.wStackedRecoverOps = _wRoot.findChild(QWidget, "stackedRecoverOps")
		self.wStackedRecoverOps.hide() #hidden for now

		self.wBtnRecoverRun = _wRoot.findChild(QWidget, "btnRecoverRun")
		self.wBtnRecoverRun.clicked.connect(self.recoverRun)

		self.wBtnRecoverStop = _wRoot.findChild(QWidget, "btnRecoverStop")
		self.wBtnRecoverStop.setVisible(False)
		self.wBtnRecoverStop.clicked.connect(lambda: self.recoverStop(self.args.devRecoverCut))


		self.wFrameDev = _wRoot.findChild(QWidget, "frameDev")
		self.wFrameDev.setVisible(False)
		self.wLabStats = _wRoot.findChild(QWidget, "labStats")

		_dispatch.sigDispatchAdded.connect(self.sessionPrepare)


		self.wBtnTraceLive.setChecked(self.args.visTracer)
		self.wBtnTraceLive.toggled.connect(lambda v: self.show(live=v))
		self.wBtnTraceShapes.setChecked(self.args.visTraceShapes)
		self.wBtnTraceShapes.toggled.connect(lambda v: self.show(shapes=v))


		self.show(self.args.visDispatch, live=self.args.visTracer, shapes=self.args.visTraceShapes)


		_dispatch.sigDeviceFound.connect(lambda devA:self.dispatchFill(devA, self.args.last))
		self.dispatchFill(None, self.args.last)
		_dispatch.getDevices()

		self.relock()



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
			self.activeSession = _session
			liveData = _session.liveData()
			liveData.coords = (0,0)
			liveData.active = False
			liveData.logTimeStart = datetime.now()
			liveData.logFeed = 0
			liveData.logPoints = 0
			liveData.logShapes = 0


			self.relock()

			self.wLabStats.setPlainText('')
			self.logDispatch("begin")
			self.wProgDispatch.setValue(0)
			self.sigProgress.emit(0)


			self.sigLive.emit(True)



#  todo 314 (trace) +0: move feed detection routines to session
	def traceFeed(self, _session, _res, _echo, _feed):
		liveData = _session.liveData()

#  todo 301 (trace) +0: show computed feed, points rate
#  todo 302 (trace) +0: show path kpi and segments metrics
		edge = re.findall("S([\d]+)", _feed)
		if edge:
			if not liveData.active and float(edge[0])!=0:
				liveData.logShapes += 1

			if float(edge[0])==0:
				self.tracer.split()

			liveData.active = (float(edge[0])!=0)



		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _feed)
		if coords:
			liveData.coords = (float(coords[0][0]), -float(coords[0][1]))
			liveData.logPoints += 1

			self.tracer.moveto(liveData.coords)


		if _res!=True:
			self.tracer.spot(True)

			if not _res:
				self.logDispatch('No device')
				return

			if _res == -1:
				self.logDispatch('Port error')
				return

			echo = ("\nwith:\n" if _echo else '') +"\n".join(_echo or [])
			self.logDispatch(f"error {_res} at:\n{_feed or 'End'}{echo}")

		liveData.logFeed += 1
		prog = liveData.logFeed/_session.pathLen()
		self.sigProgress.emit(prog)
		self.wProgDispatch.setValue(100*prog)

		self.logSession(liveData)



	def traceFinal(self, _session, _res):
		msgA = {_session.errOk:'correct', _session.errDevice:'halt', _session.errCancel:'canceled'}
		endMsg = msgA[_res] if _res in msgA else f"unknown ({_res})"
		self.logDispatch(f"{endMsg}\n")

		self.logSession(_session.liveData(), endMsg)

		msgErr = 'Connection dropped' if _session.resultRuntime[-1][0]<0 else f'Error {_session.resultRuntime[-1][0]}'
		self.devStateBlockState(_res!=_session.errDevice, msgErr)


		cDeg = 0
		cAmt = 0
		if _res!=_session.errOk and _res!=_session.errCancel:
			lastCoords = _session.liveData().coords
			lastCoords = (-lastCoords[1], lastCoords[0]) #coordsystem transform back

			cDeg = math.degrees(math.atan2(*lastCoords))
			cAmt = -math.hypot(*lastCoords)

		self.wRecDeg.setText('%.8f' % cDeg)
		self.wRecDeg.setCursorPosition(0)
		self.wRecAmt.setText('%.8f' % cAmt)
		self.wRecAmt.setCursorPosition(0)



#  todo 294 (tracer, clean) +0: check memory leak on subsequent sessions
		self.activeSession = None
		del _session

		self.relock()

		self.sigLive.emit(False)
