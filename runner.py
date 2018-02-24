from bot.settings import *
from bot.telegram_bot import Bot


if __name__ == '__main__':
	try:
		bot = Bot(TOKEN)
		bot.listen()
	except KeyboardInterrupt:
		exit()
