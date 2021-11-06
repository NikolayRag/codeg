import argparse, os, json
import logging


'''
Deal with app settings.
Loads previously saved and put commandline arguments over.
'''
# =todo 240 (api) +0: make global settings singletone
class Args():
	defaults = [
		['-defWindowFit', 0.8],
		['-defVportFit', 0.5],
		['-defVportGeoFit', .3],
		['-defVportOffset', 0.66],
	]


	appName = 'codeg'
	settingsFile = os.path.join(os.path.expanduser('~'), ".%s/%s.ini" % (appName,appName))

	args= None



	'''
	_reuseOld tells to load saved settings.
	If set, 'dst' is not required.
	'''
	def __init__(self, _reuseOld=True):
		if _reuseOld:
			self.args = self.load()

		if not self.args:
			self.args = {}


		cArgs = self.parseCmdline()

		if cArgs:
			for cArg in cArgs:
				if cArgs[cArg] != None:
					self.args[cArg] = cArgs[cArg]




	def get(self, _field, default=None):
		return self.args[_field] if (_field in self.args) else default



	def set(self, _field, _val, save=True):
		self.args[_field] = _val

		if save:
			self.save()



	'''
	Save current settings to application related file.
	'''
	def save(self):
		settings = json.dumps(self.args, sort_keys=True, indent=4)

		try:
			if not os.path.exists(os.path.dirname(self.settingsFile)):
				os.makedirs(os.path.dirname(self.settingsFile))

			f = open(self.settingsFile, 'w')
			f.write(settings)
		except:
			logging.warning('Settings could not be saved.')
			return


		f.close()



	#private

	def load(self):
		try:
			f = open(self.settingsFile, 'r')
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
			return json.loads(settingsStr)
		except:
			logging.warning('Setting file corrupt')
			return





	def parseCmdline(self):
		cParser = argparse.ArgumentParser(description= 'codeg')

		cParser.add_argument('-v', default=False, action='store_true', help='version 0')
#		cParser.add_argument('inStr', type=str, default='pwned', nargs=(None if 0 else '?'), help='Mandatory string input')

		for argn, argv in self.defaults:
			cParser.add_argument(argn, default=argv, help=argparse.SUPPRESS)

		
		cArgs = cParser.parse_args()
	
		if cArgs:
			return vars(cArgs)
		