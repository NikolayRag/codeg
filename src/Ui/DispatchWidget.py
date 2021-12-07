from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



class DispatchWidget(QObject):


	def __init__(self, _dispatch, _wRoot, _tracer=None):
		QObject.__init__(self)

		self.dispatch = _dispatch
		self.wRoot = _wRoot
		self.tracer = _tracer
