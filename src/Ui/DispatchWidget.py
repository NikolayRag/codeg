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
