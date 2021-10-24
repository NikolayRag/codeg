'''
Generalized eventFilter() control.

Accepts {event: function(event)} dict.

Function is called at given event,
 and its return value is returned by eventFilter(),
 which is reasonable for some cases.

When used, assign it to non-volatile variable, not to be GC'd
'''



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
