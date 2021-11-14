from Args import *



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



	def __init__(self, _dispatch=None):
		self.dispatcher = _dispatch



	def getDevices(self):
		if self.dispatcher:
			return self.dispatcher.getDevices()


		return {'Default': CNCNull(Args.Device.width, Args.Device.height)}



	def runDevice(self, _dev, _data, _logCB=None):
		print('Dispatch', len(_data), 'commands to', _dev)
		return
