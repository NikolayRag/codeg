import json
import serial
import serial.tools.list_ports


from ..DispatchEngine import *



class EngineArduinoGRBL(DispatchEngine):
	nameBase = 'GRBL'



	def deviceDetect(_dev, _bps):
		try:
			port = serial.Serial(_dev.device, _bps,
				timeout=2,
			    parity=serial.PARITY_NONE,
	    		stopbits=serial.STOPBITS_ONE,
	    		bytesize=serial.EIGHTBITS,
    		)

			echo = port.readline().decode()
			if not echo:
				return

			echo = port.readline().decode()
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
				cDev = EngineArduinoGRBL(portN.device, {'v':cEcho})
				instances.append(cDev)


		return instances



	def __init__(self, _name, size=None, privData=None):
		cName = f"{self.nameBase} ({_name})"
		DispatchEngine.__init__(self, cName, size, privData=privData)


		self.port = _name

