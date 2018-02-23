from bot.telegram_bot import Bot
from bot.settings.settings import *


if __name__ == '__main__':
	try:
		bot = Bot(TOKEN)
		bot.start()
	except KeyboardInterrupt:
		exit()
