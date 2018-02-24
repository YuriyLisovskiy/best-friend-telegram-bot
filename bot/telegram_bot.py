import requests
import datetime

from bot.utils.decorators import run_async


class Bot:
	
	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)
		self.greetings = ('hello', 'hi', 'greetings')
		self.now = datetime.datetime.now()
		self.today = self.now.day
		self.start_message = 'Telegram Bot\nVersion 1.0.0\nStarted listening for updates...'
		self.welcomed_users = []
	
	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {
			'timeout': timeout,
			'offset': offset
		}
		response = requests.get(self.api_url + method, params)
		if not response.json()['ok']:
			raise ValueError("Bot not found or invalid bot token.")
		return response.json()['result']
	
	def send_message(self, chat_id, text):
		method = 'sendMessage'
		params = {
			'chat_id': chat_id,
			'text': text
		}
		response = requests.post(self.api_url + method, params)
		if response.json()['ok']:
			print("Response status: sent")
		else:
			print("Response status: failed")
		return response
	
	def get_last_update(self):
		get_result = self.get_updates()
		if len(get_result) > 0:
			last_update = get_result[-1]
		else:
			last_update = None
		return last_update
	
	@staticmethod
	def check_received_message(string, data_list):
		return any(word in string for word in data_list)
	
	@staticmethod
	def get_greeting(receiver, hour):
		result = 'Good '
		if 6 <= hour < 12:
			result += 'morning'
		elif 12 <= hour < 17:
			result += 'afternoon'
		elif 17 <= hour < 23:
			result += 'evening'
		else:
			result += 'night'
		return result + ', {}'.format(receiver)
	
	@staticmethod
	def parse_message(last_update):
		if 'text' in last_update['message'].keys():
			result = last_update['message']['text']
		else:
			result = None
		return result
	
	@run_async
	def control_datetime(self):
		while True:
			if self.today != self.now.day:
				self.today = self.now.day
				self.welcomed_users.clear()
			self.now = datetime.datetime.now()
	
	def listen(self):
		new_offset = None
		listening = True
		self.control_datetime()
		print(self.start_message)
		while listening:
			self.get_updates(new_offset)
			last_update = self.get_last_update()
			if last_update:
				last_update_id = last_update['update_id']
				last_chat_id = last_update['message']['chat']['id']
				last_chat_name = last_update['message']['chat']['first_name']
				last_chat_text = self.parse_message(last_update)
				if last_chat_text:
					if self.check_received_message(last_chat_text.lower(), self.greetings):
						if last_chat_id not in self.welcomed_users:
							self.welcomed_users.append(last_chat_id)
							data = {
								'receiver': last_chat_name,
								'hour': self.now.hour
							}
							message = self.get_greeting(**data)
						else:
							message = 'Hi again.'
					else:
						message = 'Sorry, I was created only for greetings.\nSay '
						for i in range(len(self.greetings) - 1):
							message += '"' + self.greetings[i] + '", '
						message += 'or "' + self.greetings[-1] + '".'
				else:
					message = 'Sorry, I can parse only text messages.'
				self.send_message(last_chat_id, message)
				new_offset = last_update_id + 1
