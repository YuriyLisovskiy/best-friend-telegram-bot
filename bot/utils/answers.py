
GREETINGS = ('hello', 'hi', 'greetings', 'welcome', '/start')

SORRY_ANSWER = 'Sorry, I was created only for greetings.\nSay '

for i in range(len(GREETINGS) - 1):
	SORRY_ANSWER += '"' + GREETINGS[i] + '", '
SORRY_ANSWER += 'or "' + GREETINGS[-1] + '".'

RANDOM_ANSWERS = [
	'LOL',
	'KEK',
	'ROFL',
	'I don\'t understand you.',
	SORRY_ANSWER
]

INVALID_MESSAGE_ANSWER = (
	'Sorry, I can parse only text messages.',
	'Are you kidding ?',
	'-_-'
)

POSITIVE_ANSWERS = [
	"Yes",
	'Hmm, okay.',
	"Of course",
	"All right",
	"No doubts"
]

NEGATIVE_ANSWERS = [
	"No",
	"It is forbidden",
	"I do not allow",
	"Hope you`re kidding"
]

NEUTRAL_ANSWERS = [
	"I do not now yet",
	"I think yes"
]
