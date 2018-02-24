TOKEN = 'set_in_local_settings'

try:
	from bot.local_settings import *
except ImportError:
	pass
