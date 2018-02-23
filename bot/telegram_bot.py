import requests
import datetime


class Bot:
	
	def __init__(self, token):
		self.token = token
		self.api_url = "https://api.telegram.org/bot{}/".format(token)
		self.greetings = ('hello', 'hi', 'greetings', 'sup')
		self.now = datetime.datetime.now()
	
	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {
			'timeout': timeout,
			'offset': offset
		}
		response = requests.get(self.api_url + method, params)
		result_json = response.json()['result']
		return result_json
	
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
			last_update = get_result[len(get_result)]
		return last_update
	
	def start(self):
		new_offset = None
		today = self.now.day
		hour = self.now.hour
		while True:
			self.get_updates(new_offset)
			last_update = self.get_last_update()
			last_update_id = last_update['update_id']
			last_chat_text = last_update['message']['text']
			last_chat_id = last_update['message']['chat']['id']
			last_chat_name = last_update['message']['chat']['first_name']
			
			if last_chat_text.lower() in self.greetings and today == self.now.day and 6 <= hour < 12:
				self.send_message(last_chat_id, 'Good morning, {}'.format(last_chat_name))
				today += 1
			
			elif last_chat_text.lower() in self.greetings and today == self.now.day and 12 <= hour < 17:
				self.send_message(last_chat_id, 'Good afternoon, {}'.format(last_chat_name))
				today += 1
			
			elif last_chat_text.lower() in self.greetings and today == self.now.day and 17 <= hour < 23:
				self.send_message(last_chat_id, 'Good evening, {}'.format(last_chat_name))
				today += 1
			
			new_offset = last_update_id + 1
