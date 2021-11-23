# =todo 260 (module-dispatch, test) +0: test GRBL 

import serial
import serial.tools.list_ports


from ..DispatchEngine import *


class EngineArduinoGRBL(DispatchEngine):
	nameBase = 'GRBL'


	#runtime

	port = None



	def deviceDetect(_dev, _bps):
		try:
			port = serial.Serial(_dev.device, _bps,
				timeout=4,
			    parity=serial.PARITY_NONE,
	    		stopbits=serial.STOPBITS_ONE,
	    		bytesize=serial.EIGHTBITS,
    		)

			echo = port.readline().decode()
			if not echo:
				return

			echo = port.readline().decode()
			port.close()

			if echo[:5]=='Grbl ':
				return echo

		except Exception as e:
			None



	def enumerate(_defs=None):
		instances = []

		cPortsA = serial.tools.list_ports.comports()
		for portN in cPortsA:
			cRate = _defs['rate'] if 'rate' in _defs else 115200
			cEcho = EngineArduinoGRBL.deviceDetect(portN, cRate)
			if cEcho:
				cDev = EngineArduinoGRBL(
					f"{EngineArduinoGRBL.nameBase} ({portN.device})",
					privData={'port':portN.device, 'rate':cRate, 'v':cEcho}
				)
				instances.append(cDev)


		return instances



	def __init__(self, _name, privData=None):
		privData['head'] = 'F8000'
		privData['tail'] = ''
		privData['pokes'] = 2

		DispatchEngine.__init__(self, _name, privData=privData)



	def begin(self):
		try:
			self.port = serial.Serial(self.privData['port'], self.privData['rate'],
				timeout=4,
			    parity=serial.PARITY_NONE,
	    		stopbits=serial.STOPBITS_ONE,
	    		bytesize=serial.EIGHTBITS,
    		)


			echo = self.port.readline().decode()
			if echo:
				echo = self.port.readline().decode()
				if echo[:5]=='Grbl ':
					return True


		except Exception as e:
			print(f"Device \"{self.getName()}\" error")
			None



	def end(self):
		try:
			self.port and self.port.close()

		except Exception as e:
			None


		self.port = None



# =todo 259 (fix, module-dispatch) +0: test device errors
	def send(self, _data):
		try:
			self.port and self.port.write(str.encode(_data + '\n'))

			for i in range(self.privData['pokes']):
				res = self.port and self.port.readline().decode().strip()
				if res:
					return True if res=='ok' else res


		except Exception as e:
			self.end()

			return False



	def sink(self, _data):
		if not _data:
			if self.port:
				self.send(self.privData['tail'])
				self.end()

				return True


		if not self.port:
			if not self.begin():
				print(f"Device \"{self.getName()}\" unavailable")

				self.end()

				return False

			return self.send(self.privData['head'])


		res = self.send(_data)
		return res
