import random
import requests
import datetime

from bot.utils.answers import *
from bot.utils.decorators import run_async


class Bot:
	
	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)
		self.now = datetime.datetime.now()
		self.today = self.now.day
		self.start_message = 'Telegram Bot\nVersion 1.0.0\nStarted listening for updates...'
		self.welcomed_users = []
		self.serving_users = []
		self.last_update = None
	
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
	
	def send_message(self, chat_id, username, text):
		method = 'sendMessage'
		params = {
			'chat_id': chat_id,
			'text': text
		}
		response = requests.post(self.api_url + method, params)
		if response.json()['ok']:
			print("Response sent, receiver: @{}, time: {}".format(username, datetime.datetime.now()))
		else:
			print("Response failed, receiver: @{}, time: {}".format(username, datetime.datetime.now()))
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
	
	@staticmethod
	def is_message(last_update):
		return 'message' in last_update
	
	@run_async
	def control_datetime(self):
		while True:
			if self.today != self.now.day:
				self.today = self.now.day
				self.welcomed_users.clear()
			self.now = datetime.datetime.now()
	
	@run_async
	def start_serve_user(self, chat_id):
		last_update, temp_update = None, None
		while True:
			temp_update = self.last_update
			if last_update != temp_update:
				last_update = temp_update
				if self.is_message(last_update):
					last_chat_id = last_update['message']['chat']['id']
					if chat_id == last_chat_id:
						last_chat_name = last_update['message']['chat']['first_name']
						last_chat_text = self.parse_message(last_update)
						if last_chat_text:
							print(last_chat_text)
							if self.check_received_message(last_chat_text.lower(), GREETINGS):
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
								answers = RANDOM_ANSWERS
								if '?' not in last_chat_text and last_chat_text != '?':
									answers.append(POSITIVE_ANSWERS + NEGATIVE_ANSWERS + NEUTRAL_ANSWERS)
								elif last_chat_text == '?':
									answers = ['What do you mean by sending me a question mark, {} ?'.format(last_chat_name)]
								message = random.choice(answers)
						else:
							message = random.choice(INVALID_MESSAGE_ANSWER)
						self.send_message(last_chat_id, last_update['message']['chat']['username'], message)
	
	def listen(self):
		new_offset = None
		listening = True
		self.control_datetime()
		print(self.start_message)
		while listening:
			self.get_updates(new_offset)
			self.last_update = self.get_last_update()
			if self.last_update:
				last_update_id = self.last_update['update_id']
				if self.is_message(self.last_update):
					last_chat_id = self.last_update['message']['chat']['id']
					if last_chat_id not in self.serving_users:
						self.serving_users.append(last_chat_id)
						self.start_serve_user(last_chat_id)
				new_offset = last_update_id + 1
