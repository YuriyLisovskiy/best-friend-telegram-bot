TOKEN = 'set_in_local_settings'

try:
	from .local_settings import *
except ImportError:
	pass
