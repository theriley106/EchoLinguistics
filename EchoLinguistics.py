import sys
import os
import requests
import awsIntegration
import random
import json

languageList = json.loads(open("supportedLanguages.json").read())

mp3File = 'finalfile.mp3'
def generateURL(keyWords, region):
	keyWords = keyWords.replace(" ", "%20")
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}".format(keyWords, region)

def generateSSML(text, region=None):
	if region == None:
		region = random.choice(languageList)['Abbreviation']
	url = generateURL(text, region.lower())
	mp3File = saveMP3(url)
	editMP3(mp3File)
	fileName = awsIntegration.uploadFile(mp3File)
	os.system('rm {}'.format(mp3File))
	return fileName

def saveMP3(mp3URL):
	#return MP3 file name
	mp3File = "{}.mp3".format(str(random.randint(1, 999999)))
	mp3File = 'finalfile.mp3'
	#calls it a random file name to later delete
	with open(mp3File, 'wb') as f:
		#this saves the response locally as an actual mp3 file
		f.write(requests.get(mp3URL).content)
	return mp3File

def editMP3(mp3File):
	os.system("ffmpeg -speed 16 -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 -vol 1026 tmp.mp3 && mv tmp.mp3 {}".format(mp3File, mp3File))
	#this is the regular FFMPEG command to convert it to a playable audio file.  Notice the tmp and mv tmp.mp3, because -i will overwrite the file as you go along.

url = generateSSML("""Its Friday, Friday
Gotta get down on Friday
Everybody's lookin' forward to. the. weekend.  Parteeeing. Parteeeing. waaaaaah. Parteeeing. Parteeeing. waaaaaaah.  looking forward to the weekend.  yeah""", 'en')
print url



