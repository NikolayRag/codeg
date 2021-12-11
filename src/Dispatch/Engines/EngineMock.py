from ..DispatchEngine import *


class EngineMock(DispatchEngine):
	nameBase = 'Mockup'


	def enumerate(_defs=None):
		iniDefs = {'50x50':(50,50), '200x200':(200,200)}
		return iniDefs



	def __init__(self, _name, privData=None):
		self.size = privData

		_name = f"{self.nameBase} {_name}"
		DispatchEngine.__init__(self, _name)



	def sink(self, _data):
		return True



	def test(self):
		return True
