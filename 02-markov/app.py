import math
import pprint
import random
import re
import requests

books = [
	# Pride and Prejudice
	'https://www.gutenberg.org/cache/epub/1342/pg1342.txt',

	# Emma
	'https://www.gutenberg.org/cache/epub/158/pg158.txt',

	# Persuasion
	'https://www.gutenberg.org/cache/epub/105/pg105.txt',

	# Northanger Abbey
	'https://www.gutenberg.org/cache/epub/121/pg121.txt'

	# Sense and Sensibility
	'https://www.gutenberg.org/cache/epub/161/pg161.txt'
]

def normalize(options):
	totalWeight = 0
	for word, weight in options.items():
		totalWeight = totalWeight + weight

	normalizedOptions = {}
	for word, weight in options.items():
		normalizedOptions[word] = weight / totalWeight

	return normalizedOptions

def pick(options):
	normalizedOptions = normalize(options)
	r = random.random()

	for option, weight in normalizedOptions.items():
		r = r - weight

		if r <= 0:
			return option

	return list(normalizedOptions.keys())[-1]

def sortedOptions(options):
	return sorted(options.items(), key=lambda item: item[1], reverse=True)

def temperature(options, t):
	normalizedOptions = normalize(options)

	result = {}
	for word, weight in options.items():
		result[word] = math.pow(weight, t)

	return normalize(result)

def topK(options, k):
	return normalize(dict(sortedOptions(options)[0:k]))

def topP(options, p):
	normalizedOptions = normalize(dict(sortedOptions(options)))

	result = {}
	weightSoFar = 0
	for word, wordP in normalizedOptions.items():
		result[word] = wordP
		weightSoFar = weightSoFar + wordP

		if weightSoFar >= p:
			break;

	return normalize(result)

def accumulateMarkovData(url, model):
	r = requests.get(url)

	lastWord = False
	maxCount = 0
	numDelim = 0
	for word in r.text.split():
		if word == '***':
			numDelim = numDelim + 1

		if numDelim != 2:
			continue

		if re.match(r'[A-Z]{2,}', word):
			continue

		if re.match(r'[0-9]+', word):
			continue

		word = re.sub(r'[^a-zA-Z0-9\.\,\;\:]', '', word)
		word = word.strip()

		if lastWord and word != '':
			if not lastWord in model: model[lastWord] = {}
			if not word in model[lastWord]: model[lastWord][word] = 0

			model[lastWord][word] = model[lastWord][word] + 1

			if model[lastWord][word] > maxCount:
				maxCount = model[lastWord][word]

		lastWord = word

words = {}

for book in books:
	accumulateMarkovData(book, words)

curWord = 'Once'
for x in range(100):
	print (f'{curWord} ', end='', flush=True)

	curWord = pick(temperature(topP(words[curWord], .7), .01))

print(curWord)
