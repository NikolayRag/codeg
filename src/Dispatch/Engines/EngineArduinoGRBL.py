import serial
import serial.tools.list_ports


from ..DispatchEngine import *


class EngineArduinoGRBL(DispatchEngine):
	nameBase = 'GRBL'


	#runtime

	privData = None
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
		DispatchEngine.__init__(self, _name, privData=privData)



