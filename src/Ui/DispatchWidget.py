from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


from .Tracer import *



class DispatchWidget(QObject):
	sigTracerProgress = Signal(float)

	sigDevChange = Signal(str, object)
	sigDispatchFire = Signal(str)



	def devChanged(self, i):
		_name = self.wListDevs.currentText()
		_enabled = self.wListDevs.currentData()

		print(f"Device changed to \"{_name}\"", 'mock' if not _enabled else '')

		self.args.last = _name

#  todo 257 (ux) +0: handle nonexistent device
		self.wBtnDispFire.setEnabled(_enabled)

		self.sigDevChange.emit(_name, _enabled)



	def __init__(self, _wRoot, _dispatch, _args, _viewport):
		QObject.__init__(self)

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args

		self.wFrameDev = _wRoot.findChild(QWidget, "frameDev")
		self.wLabStats = _wRoot.findChild(QWidget, "labStats")


		self.tracer = Tracer(_viewport, [self.wFrameDev, self.wLabStats])


### setup ###

		self.wBtnRescan = _wRoot.findChild(QWidget, "btnRescan")
		self.wListDevs = _wRoot.findChild(QComboBox, "listDevs")
		self.wBtnDispFire = _wRoot.findChild(QWidget, "btnDispFire")


		self.wBtnRescan.clicked.connect(_dispatch.getDevices)
		self.wListDevs.currentIndexChanged.connect(self.devChanged)
		self.wBtnDispFire.clicked.connect(lambda: self.sigDispatchFire.emit(self.wListDevs.currentText()))


		self.sigTracerProgress = self.tracer.sigProgress

		_dispatch.sigDispatchAdded.connect(self.tracer.prepare)
		_dispatch.sigDispatchBegin.connect(self.tracer.reset)
		_dispatch.sigDispatchSent.connect(self.tracer.feed)
		_dispatch.sigDispatchFinish.connect(self.tracer.final)


		self.wBtnTraceLive = _wRoot.findChild(QWidget, "btnTraceLive")
		self.wBtnTraceLive.setChecked(self.args.visTracer)

		self.wBtnTraceShapes = _wRoot.findChild(QWidget, "btnTraceShapes")
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



	def traceReset(self):
		self.tracer.reset()
