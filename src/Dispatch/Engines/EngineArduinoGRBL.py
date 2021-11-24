# =todo 260 (module-dispatch, test) +0: test GRBL 

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
			iniDefs[portN.device] = {'port':portN.device, 'rate':cRate}


		return iniDefs



	def __init__(self, _name, privData=None):
		privData['head'] = 'F8000'
		privData['tail'] = ''
		privData['pokes'] = 2

		_name = f"{self.nameBase} ({_name})"
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



	def test(self):
		if self.port:
			return True


		if not self.begin():
			return False


		self.end()

		return True
