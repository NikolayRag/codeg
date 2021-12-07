from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


from .Tracer import *



class DispatchWidget(QObject):
	sigTracerProgress = Signal(float)

	sigDispatchFire = Signal()





	def __init__(self, _wRoot, _dispatch, _args, _viewport):
		QObject.__init__(self)

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args

		self.wFrameDev = _wRoot.findChild(QWidget, "frameDev")
		self.wLabStats = _wRoot.findChild(QWidget, "labStats")


		self.tracer = Tracer(_viewport, [self.wFrameDev, self.wLabStats])


### setup ###

		self.wBtnDispFire = _wRoot.findChild(QWidget, "btnDispFire")


		self.wBtnDispFire.clicked.connect(self.sigDispatchFire)


		self.sigTracerProgress = self.tracer.sigProgress

		self.slotPrepare = self.tracer.prepare
		self.slotReset = self.tracer.reset
		self.slotFeed = self.tracer.feed
		self.slotFinal = self.tracer.final


		self.wBtnTraceLive = self.wRoot.findChild(QWidget, "btnTraceLive")
		self.wBtnTraceLive.setChecked(self.args.visTracer)

		self.wBtnTraceShapes = self.wRoot.findChild(QWidget, "btnTraceShapes")
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
