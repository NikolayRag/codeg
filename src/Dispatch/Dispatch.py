import serial
import serial.tools.list_ports



# =todo 60 (module-dispatch) +0: show gcodes live proto
# =todo 61 (module-dispatch) +0: CNC control
# =todo 62 (module-dispatch) +0: live device control
# -todo 64 (module-dispatch) +0: dispatch queue
# -todo 68 (module-dispatch) +0: queue control
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



	def deviceInfo(_dev):
		if _dev not in self.listPorts:
			return

		return[
			self.listPorts[_dev].device,
			self.listPorts[_dev].apply_usb_info(),
			self.listPorts[_dev].description,
			self.listPorts[_dev].hwid,
			self.listPorts[_dev].interface,
			self.listPorts[_dev].location,
			self.listPorts[_dev].manufacturer,
			self.listPorts[_dev].name,
			self.listPorts[_dev].pid,
			self.listPorts[_dev].product,
			self.listPorts[_dev].serial_number,
			self.listPorts[_dev].usb_description(),
			self.listPorts[_dev].usb_info(),
			self.listPorts[_dev].vid
		]



	def runDevice(self, _dev, _logCB=None):
		if _dev not in self.listPorts:
			print('Invalid port', _dev)
			return

		try:
			port = serial.Serial(_dev, 115200)
		except Exception as e:
			print("Port ", _dev, " error")

			return


		port.readline().decode()

		toSendString = self.data.getG()

		cursorChar = '>'
		cursorLen = 1

		        
		gLines = toSendString.splitlines()+['']

		for cLine in gLines:
			inString = ''

			inString = port.readline().decode().strip()
			if inString:
				_logCB and _logCB('<' + inString)

			_logCB and _logCB('>' + cLine)
			port.write(str.encode(cLine + '\n'))


		port.close()

		return True
