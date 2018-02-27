
GREETINGS = ('hello', 'hi', 'greetings', '/start')

SORRY_ANSWER = 'Sorry, I was created only for greetings.\nSay '

for i in range(len(GREETINGS) - 1):
	SORRY_ANSWER += '"' + GREETINGS[i] + '", '
SORRY_ANSWER += 'or "' + GREETINGS[-1] + '".'

RANDOM_ANSWERS = ('LOL', 'KEK', 'ROFL', SORRY_ANSWER)

INVALID_MESSAGE_ANSWER = ('Sorry, I can parse only text messages.', 'Are you kidding ?')
