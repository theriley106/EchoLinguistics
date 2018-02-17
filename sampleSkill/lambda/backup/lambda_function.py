import os
import re
import shutil
import stat
import datetime
import sys
import requests
import random
import json
import tinys3
import time


lambda_tmp_dir = '/tmp'
ffmpeg_bin = "{0}/ffmpeg.linux64".format(lambda_tmp_dir)
shutil.copyfile('/var/task/ffmpeg.linux64', ffmpeg_bin)

languageList = json.loads(open("supportedLanguages.json").read())

def uploadFile(fileName):
	start = time.time()
	finalFileName = fileName.split('/')[-1]
	conn = tinys3.Connection(ACCESS_KEY,SECRET_KEY,tls=True)
	conn.upload(finalFileName, open(fileName,'rb'), BUCKET_ID)
	return "<speak><audio src='https://s3.amazonaws.com/{}/{}'/></speak>".format(BUCKET_ID, fileName)

def generateURL(keyWords, region):
	print keyWords
	print region
	keyWords = keyWords.replace(" ", "%20")
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}".format(keyWords, region)

def generateSSML(text, region=None):
	if region == None:
		region = random.choice(languageList)['Abbreviation']
	url = generateURL(text, region.lower())
	print url
	mp3File = saveMP3(url, region)
	editMP3(mp3File)
	fileName = uploadFile(mp3File)
	os.system('rm {}'.format(mp3File))
	print("Successfully downloaded")
	return fileName

def saveMP3(mp3URL, region):
	#return MP3 file name
	mp3File = '/tmp/{}.mp3'.format(region)
	#calls it a random file name to later delete
	with open(mp3File, 'wb') as f:
		#this saves the response locally as an actual mp3 file
		f.write(requests.get(mp3URL).content)
	return mp3File

def editMP3(mp3File):
	os.system("{} -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 -y -vol 1026 /tmp/tmp.mp3 && mv /tmp/tmp.mp3 {}".format(ffmpeg_bin, mp3File, mp3File))
	#this is the regular FFMPEG command to convert it to a playable audio file.  Notice the tmp and mv tmp.mp3, because -i will overwrite the file as you go along.



def lambda_handler(event, context):
	try:
		region = event["Region"]
	except:
		region = None
	url = generateSSML(event["Text"], region=region)
