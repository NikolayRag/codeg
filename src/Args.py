import argparse, os, json
import logging


'''
Deal with app settings.
Loads previously saved and put commandline arguments over.
'''
class ArgBlock():
	_name = None
	_data = {}
	_saveCB = None


	def __init__(self, _name, _data=[]):
		self._name = _name
		self._data = {}

		for n, d in _data:
			self._setData(n, d)


	def _setCB(self, _cb):
		self._saveCB = _cb


	def _getName(self):
		return self._name


	def _setData(self, _name, _data):
		self._data[_name] = _data[1:]

		setattr(self, _name, _data[0])


	def _getData(self):
		return dict(self._data)


	def __getattr__(self, _name):
		return self.__dict__[_name]


	def __setattr__(self, _name, _val):
		self.__dict__[_name] = _val 

		self._saveCB and self._saveCB()




class Args():
	_iniFile = None

	_args = []



	def _fillFields(self, _fields):
		for blockN, blockV in _fields.items():
			if not hasattr(Args, blockN):
				cBlock = ArgBlock(blockN)
				setattr(Args, blockN, cBlock)

				Args._args.append(cBlock)


			cBlock = getattr(Args, blockN)
			for argN, argV in blockV.items():
				cBlock._setData(argN, argV)



	def _parseCmdline(self, _args):
		cParser = argparse.ArgumentParser()

		for cVar in _args._getData():
			cParser.add_argument(f"-{cVar}", default=getattr(_args, cVar), type=type(cVar))
		
		try:
			cArgs = cParser.parse_args()
		except:
			return
		

		for cVar in _args._getData():
			setattr(_args, cVar, getattr(cArgs, cVar))

	def __init__(self, _field, _iniFile=None):
		self._fillFields(_field)


		if _iniFile:
			self._iniFile = os.path.join(os.path.expanduser('~'), ".%s/%s.ini" % (_iniFile,_iniFile))
			self._load()


# -todo 243 (API, app) +0: parse command line
#		self._parseCmdline(_prefs)


		for cBlock in Args._args:
			cBlock._setCB(self._save)



	'''
	Save current settings to application related file.
	'''
	def _save(self):
		saveData = {}

		for cBlock in Args._args:
			if not cBlock._saveCB:
				continue

			cFieldsA = {}
			for cField in cBlock._getData():
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
			cBlock = getattr(self, blockN) if hasattr(self, blockN) else ArgBlock(blockN)

			for fieldN, fieldV in blockV.items():
				setattr(cBlock, fieldN, fieldV)


	def _list():
		return list(Args._args)
