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

			inString = port.readline().decode()
			if inString.strip():
				print('<', inString)

			print('>', cLine)
			port.write(str.encode(cLine + '\n'))


		port.close()

		return True
