# -todo 298 (device, fix) +2: operate device nonblocking

# -todo 260 (module-dispatch, fix) +5: GRBL realtime control
#  todo 320 (device) +0: device x/y scale factor
import serial
import serial.tools.list_ports


from ..DispatchEngine import *


class EngineArduinoGRBL(DispatchEngine):
	nameBase = 'GRBL'


	#runtime

	port = None



	def enumerate(_defs=None):
		iniDefs = {}

		cPortsA = serial.tools.list_ports.comports()
		for portN in cPortsA:
			cRate = _defs['rate'] if 'rate' in _defs else 115200
			cTimeout = _defs['timeout'] if 'timeout' in _defs else 30
			iniDefs[portN.device] = {'port':portN.device, 'rate':cRate, 'timeout':cTimeout}


		return iniDefs



	def __init__(self, _name, privData=None):
		privData['timeoutInit'] = 4

		_name = f"{self.nameBase} ({_name})"
		DispatchEngine.__init__(self, _name, privData=privData)



	def begin(self, _timeout):
		try:
			self.port = serial.Serial(self.privData['port'], self.privData['rate'],
				timeout=_timeout,
			    parity=serial.PARITY_NONE,
	    		stopbits=serial.STOPBITS_ONE,
	    		bytesize=serial.EIGHTBITS,
    		)


			echo = self.port.readline().decode()
			if not echo:
				return

			echo = self.port.readline().decode()
			if echo[:5]!='Grbl ':
				return




			return True


		except Exception as e:
			None



	def end(self):
		try:
			self.port and self.port.close()

		except Exception as e:
			self.lastError((DispatchEngine.errPort, []))


		self.port = None


#  todo 310 (module-dispatch, fix) +0: GRBL write-ahead streaming mode
	def send(self, _data):
		try:
			self.port and self.port.write(str.encode(_data + '\n'))

			outRes = []
			while 1:
				res = self.port and self.port.readline().decode().strip()
				if not res: #timeout
					res = DispatchEngine.errPort
					break

				if res=='ok':
					res = True
					break

				if res[:6]=='error:':
					res = int(res[6:])
					break

				outRes.append(res)


			return (res, outRes)


		except Exception as e:
			return (DispatchEngine.errPort, [])



#  todo 345 (device) +0: split device disconnect functions
	def sink(self, _data):
		if _data == False: #instant disconnect
			self.end()

			return (DispatchEngine.errPort, [])


		if not _data: #normal end
			if self.port:
				self.send('G4 P0.01')
				
				self.end()

			return (True, [])


		if not self.port: #normal start
			if not self.begin(self.privData['timeout']):
				print(f"Device \"{self.getName()}\" unavailable")

				self.end()

				return (DispatchEngine.errPort, [])


		res = self.send(_data)
		if res[0] != True:
			self.end()

		return res



	def test(self):
		#in use, assumed valid
		if self.port:
			return True


		if not self.begin(self.privData['timeoutInit']):
			return False


		res = self.send("$$")
		if res[0] != True:
			self.end()
			return False

		cX, cY = self.getPlate()
		for cOption in res[1]:
			if cOption[:5] == '$130=':
				cX = float(cOption[5:])
			if cOption[:5] == '$131=':
				cY = float(cOption[5:])

		self.size = (cX, cY)


		res = self.send("G91 X0Y0")
		self.lastError(res)


		self.end()

		return True
