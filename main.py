import boto
import boto.s3
import sys
from boto.s3.key import Key
import requests

def generateURL(keyWords):
	keyWords = keyWords.replace(" ", "%20")
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl=en".format(keyWords)

def editMP3(mp3File):


doc = requests.get(generateURL("this actually works somehow what the fuck"))

with open('movie.mp3', 'wb') as f:
	f.write(doc.content)