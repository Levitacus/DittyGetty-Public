import json, sys, os, errno, click

APP_NAME = 'dittygetty'

class Config(dict):
	"""Does the JSON handling"""
	def __init__(self, *args, **kwargs):
		# gives the path to the JSON file, which is where this is located.
		#self.config = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])).join('config.json')

		if not os.path.exists(click.get_app_dir(APP_NAME)):
			os.makedirs(click.get_app_dir(APP_NAME))
		self.config = os.path.join(click.get_app_dir(APP_NAME), 'config.json')
		#self.config = os.path(os.curdir()) + 'config.json'
        
        
		super(Config, self).__init__(*args, **kwargs)
		
	def load(self):
		"""load a JSON config file from disk"""
		try:
			with open(self.config, 'r') as f:
				self.update(json.loads(f.read()))
		except errno.ENOENT:
			print "ENOENT error"
			pass
		except Exception as e:
			print e
	
	def save(self):
		"""Save a JSON config file to disk"""
		#self.config.ensure()
		with open(self.config, 'w') as f:
			f.write(json.dumps(self))
