# =todo 17 (spec, module-dispatch) +0: send to serial-usb (arduino)
import serial
import serial.tools.list_ports



class Dispatch():
	listPorts = []
	port = None

	data = None


	def __init__(self, _data):
		self.data = _data



	def getDevices(self):
		cPortsA = serial.tools.list_ports.comports()
		self.listPorts = {port.device: port for port in cPortsA}

		return({port.device: port.description for port in cPortsA})



	def runDevice(self, _dev):
		cPortsA = serial.tools.list_ports.comports()
		self.listPorts = {port.device: port for port in cPortsA}

		if _dev not in self.listPorts:
			return False


		print(self.listPorts[_dev])

		return True
