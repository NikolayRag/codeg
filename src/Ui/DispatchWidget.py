from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



class DispatchWidget(QObject):


	def __init__(self, _wRoot, _dispatch, _args, _tracer=None):
		QObject.__init__(self)

		self.wRoot = _wRoot
		self.dispatch = _dispatch
		self.args = _args
		self.tracer = _tracer

### setup ###

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
