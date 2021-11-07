import argparse, os, json
import logging


'''
Deal with app settings.
Loads previously saved and put commandline arguments over.
'''
# =todo 240 (api) +0: make global settings singletone
class ArgBlock():
	_name = None
	_fields = {}
	_saveCB = None


#	def __setitem__(self, _name):
	def __init__(self, _name):
		self._name = _name
		self._fields = {}


	def _setCB(self, _cb):
		self._saveCB = _cb


	def _setData(self, _name, _data):
		self._fields[_name] = _data


	def _getName(self):
		return self._name

	def _getFields(self):
		return dict(self._fields)


	def __setattr__(self, _name, _val):
		self.__dict__[_name] = _val 

		self._saveCB and self._saveCB()



class Args():
	_iniFile = None

	_args = []



	def fillFields(self, _defaults, _store=True):
		for blockN, blockV in _defaults.items():
			if not hasattr(Args, blockN):
				cBlock = ArgBlock(blockN)
				setattr(Args, blockN, cBlock)

				self._args.append(cBlock)


			cBlock = getattr(Args, blockN)
			for argN, argV in blockV.items():
				setattr(cBlock, argN, argV)

				cBlock._setData(argN, _store)



	def parseCmdline(self, _defs):
		cParser = argparse.ArgumentParser(description= 'codeg')

		cParser.add_argument('-v', default=False, action='store_true')
#		cParser.add_argument('inStr', type=str, default='pwned', nargs=(None if 0 else '?'), help='Mandatory string input')

		for block in self._args:
			for argn,argv in vars(block).items():
				cParser.add_argument(f"-{argn}", default=argv, help=argparse.SUPPRESS)

		
		cArgs = cParser.parse_args()

		if cArgs:
			return vars(cArgs)
		


	def __init__(self, _defaults, _field, _iniFile=None):
		self.fillFields(_defaults)
		self.fillFields(_field, False)


		if _iniFile:
			self._iniFile = os.path.join(os.path.expanduser('~'), ".%s/%s.ini" % (_iniFile,_iniFile))
			self._load()


#		self.parseCmdline(_defaults)


		for cBlock in self._args:
			cBlock._setCB(self._save)



	'''
	Save current settings to application related file.
	'''
	def _save(self):
		saveData = {}

		for cBlock in self._args:
			cFieldsA = {}
			for cField in cBlock._getFields():
				cFieldsA[cField] = getattr(cBlock, cField)

			saveData[cBlock._getName()] = cFieldsA


		settings = json.dumps(saveData, sort_keys=True, indent=4)

		try:
			if not os.path.exists(os.path.dirname(self._iniFile)):
				os.makedirs(os.path.dirname(self._iniFile))

			f = open(self._iniFile, 'w')
			f.write(settings)
		except:
			logging.warning('Settings could not be saved.')
			return


		f.close()



	#private

	def _load(self):
		try:
			f = open(self._iniFile, 'r')
		except:
			logging.warning('No stored settings found.')
			return


		try:
			settingsStr = f.read()
		except:
			logging.warning('Setting file couldn\'t be read')
			return

		f.close()


		try:
			filesSettings = json.loads(settingsStr)
		except:
			logging.warning('Setting file corrupt')
			return


		for blockN, blockV in filesSettings.items():
			cBlock = getattr(self, blockN)

			for fieldN, fieldV in blockV.items():
				setattr(cBlock, fieldN, fieldV)
