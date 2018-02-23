import requests
import datetime


class Bot:
	
	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)
		self.greetings = ('hello', 'hi', 'greetings')
		self.now = datetime.datetime.now()
	
	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {
			'timeout': timeout,
			'offset': offset
		}
		response = requests.get(self.api_url + method, params)
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
	
	def is_greeting(self, string):
		return any(word in string for word in self.greetings)
	
	def get_greeting(self, receiver, day, hour):
		result = ''
		if day == self.now.day and 6 <= hour < 12:
			result = 'Good morning, {}'.format(receiver)
			day += 1
		if day == self.now.day and 12 <= hour < 17:
			result = 'Good afternoon, {}'.format(receiver)
			day += 1
		if day == self.now.day and 17 <= hour < 23:
			result = 'Good evening, {}'.format(receiver)
			day += 1
		if day == self.now.day and (23 <= hour or 0 <= hour < 6):
			result = 'Good night, {}'.format(receiver)
			day += 1
		if day > self.now.day:
			result = 'Hello again.'
		return result
	
	def listen(self):
		new_offset = None
		today = self.now.day
		hour = self.now.hour
		while True:
			self.get_updates(new_offset)
			last_update = self.get_last_update()
			if last_update:
				last_update_id = last_update['update_id']
				last_chat_text = last_update['message']['text']
				last_chat_id = last_update['message']['chat']['id']
				last_chat_name = last_update['message']['chat']['first_name']
				
				if self.is_greeting(last_chat_text.lower()):
					data = {
						'receiver': last_chat_name,
						'day': today,
						'hour': hour
					}
					message = self.get_greeting(**data)
				else:
					message = 'Sorry, I was created only for greetings.\nSay '
					for i in range(len(self.greetings) - 1):
						message += '"' + self.greetings[i] + '", '
						message += 'or "' + self.greetings[-1] + '".'
					
				self.send_message(last_chat_id, message)
				new_offset = last_update_id + 1
