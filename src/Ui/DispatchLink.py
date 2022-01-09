from PySide2.QtCore import *


from .DispatchSession import *


'''
Interface for separate Dispatch
Dispatch connected either inline, or as app link
'''

#  todo 18 (API, module-dispatch, v2) +0: remote dispatcher
#  todo 258 (module-dispatch, error, ux) +0: handle retries
class DispatchLink(QObject):
	sigDeviceFound = Signal(str)
	sigDispatchAdded = Signal(object)


	dispatcher = None
	fallbackPlate = None


	#  todo 335 (dispatch, device) +0: move g-in/out to config
	gIn = ['G90', 'M4']
	gOut = ['M5', 'G0 X0Y0']
	gPause = ['M5']
	gResume = ['M4']

	#runtime

	allSessions = []



	def __init__(self, _fallbackPlate=(100,100), _dispatch=None):
		QObject.__init__(self)

		self.dispatcher = _dispatch
		self.fallbackPlate = _fallbackPlate


		self.allSessions = []



	def getDevices(self):
		if self.dispatcher:
			Thread(target=lambda: self.dispatcher.deviceList(self.sigDeviceFound.emit)).start()



	def sessionIgnite(self):
		if self.allSessions:
			self.allSessions[0].start()



	def sessionFinish(self, _session, _res):
		if self.allSessions[0] == _session:
			self.allSessions = self.allSessions[1:]

			self.sessionIgnite()

		else:
			print('Dispatch out of order')



	def sessionStart(self, _dev, _meta, _data, gIn=None, gOut=None, live=False):
		if not self.dispatcher:
			print ('No dispatcher')
			return

		def bindDev(_d):
			return self.dispatcher.deviceSend(_dev, _d)

		cSession = DispatchSession(bindDev, _meta, _data, gIn=gIn or self.gIn, gOut=gOut or self.gOut, gPause=self.gPause, gResume=self.gResume, live=live)

		if live:
			return cSession


		cSession.sigFinish.connect(lambda res: self.sessionFinish(cSession, res))
		self.sigDispatchAdded.emit(cSession)

		self.allSessions.append(cSession)
		if len(self.allSessions)==1:
			self.sessionIgnite()



	def devicePlate(self, _dev=None):
		size = _dev and self.dispatcher and self.dispatcher.deviceSize(_dev)

		return size or self.fallbackPlate



	def deviceState(self, _dev):
		if not self.dispatcher:
			return (False, [])

		return self.dispatcher.deviceLastState(_dev)
