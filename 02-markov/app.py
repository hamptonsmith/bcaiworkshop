import pprint
import random
import re
import requests

def chooseWord(options):
	chances = 0
	for weight in options.values(): chances += weight

	roll = random.random()  # number between 0 and 1
	for word, chance in options.items():
		roll -= (chance / chances)

		if roll <= 0: return word

	return array(options.keys())[-1]

def addsTextToModel(url, model):

	delimeterCt = 0
	lastToken = ''
	for token in requests.get(url).text.split():
		if token == '***': delimeterCt += 1
		if delimeterCt != 2: continue

		if not lastToken in model: model[lastToken] = {}
		if not token in model[lastToken]: model[lastToken][token] = 0

		model[lastToken][token] += 1

		lastToken = token

	return model

model = {}

addsTextToModel('https://www.gutenberg.org/cache/epub/1342/pg1342.txt', model)
addsTextToModel('https://www.gutenberg.org/cache/epub/158/pg158.txt', model)
addsTextToModel('https://www.gutenberg.org/cache/epub/161/pg161.txt', model)
addsTextToModel('https://www.gutenberg.org/cache/epub/105/pg105.txt', model)

curWord = 'Once'
for x in range(100):
	print(f'{curWord} ', end='', flush=True)

	curWord = chooseWord(model[curWord])

pprint.pp(model['play'])