'''
Generalized eventFilter() control.

Accepts {[QEvent.Type|True]: function(event)} dict,
 using True to accept any event type.

Function is called at given event,
 and its return value is returned by eventFilter(),
 which is reasonable for some cases.

When used, assign it to non-volatile variable, not to be GC'd
'''
# -todo 373 (clean) +0: store instance at class scope to prevent filter from GC



from PySide2.QtCore import *


class BindFilter(QObject):
	eventTypes = {}


	def __init__(self, _etypes):
		QObject.__init__(self)

		self.eventTypes = dict(_etypes)



	def eventFilter(self, _o, _e):
		cType = _e.type() 

		if cType not in self.eventTypes:
			if True in self.eventTypes:
				cType = True

			else:
				return False

#  todo 375 (issue) +0: consider passing affected object to provided function
		fn = self.eventTypes[cType]

		return bool(fn(_e))
