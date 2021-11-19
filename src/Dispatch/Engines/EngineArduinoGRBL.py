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




	@classmethod
	def enumerate(it, _defSize=None):
		if not it.instances:
			it.instances = []

			cPortsA = serial.tools.list_ports.comports(include_links=True)
			for portN in cPortsA:
				cEcho = it.deviceDetect(portN, 115200)
				if cEcho:
					cDev = it(portN.device, _defSize, {'v':cEcho})
					it.instances.append(cDev)


		return it.instances



	def __init__(self, _name, _size, _privData=None):
		cName = f"{self.nameBase} ({_name})"
		DispatchEngine.__init__(self, cName, _size or self.sizeBase, _privData)


		self.port = _name

