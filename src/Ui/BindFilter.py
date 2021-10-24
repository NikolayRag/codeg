from PySide2.QtCore import *


class BindFilter(QObject):
	eventTypes = {}


	def __init__(self, _etypes):
		QObject.__init__(self)

		self.eventTypes = dict(_etypes)



	def eventFilter(self, _o, _e):
		if _e.type() in self.eventTypes:
			fn = self.eventTypes[_e.type()]
			return bool(fn(_e))


		return False
