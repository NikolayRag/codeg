class CNCNull():
	size = None



	def __init__(self, _width, _height):
		self.size = (_width, _height)



	def getPlate(self):
		return self.size




# Interface for separate Dispatch
# Dispatch connected either inline, or as app link
#  todo 18 (api, module-dispatch, v2) +0: standalone dispatcher over *cloud*
class DispatchLink():
	dispatcher = None
	defaults = {}


	def __init__(self, _defaults, _dispatch=None):
		self.dispatcher = _dispatch
		self.defaults = _defaults



	def getDevices(self):
		devs = {}
		for devN, devDim in self.defaults.items():
			devs[devN] = CNCNull(*devDim)


		if self.dispatcher:
			devs = {**devs, **self.dispatcher.getDevices()}

		return devs



	def runDevice(self, _dev, _data, _logCB=None):
		print('Dispatch', len(_data), 'commands to', _dev)
		return
