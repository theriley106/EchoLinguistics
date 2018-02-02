import os
import shutil
import stat
import datetime
import requests
import awsIntegration
import random
import json

lambda_tmp_dir = '/tmp'
#Amazon only lets you write to /tmp in Lambda
ffmpeg_bin = "{0}/ffmpeg.linux64".format(lambda_tmp_dir)
#Sets location of ffmpeg
shutil.copyfile('/var/task/ffmpeg.linux64', ffmpeg_bin)
#copies file
os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)
#basically chmod +x

languageList = json.loads(open("supportedLanguages.json").read())
#Json file containing all of the supported languages

def generateURL(keyWords, region):
	#generates google translate url containing mp3 file
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}".format(keyWords.replace(" ", "%20"), region)

def saveMP3(mp3URL, region):
	#return MP3 file name
	mp3File = '/tmp/{}.mp3'.format(region)
	#calls it a random file name to later delete
	with open(mp3File, 'wb') as f:
		#this saves the response locally as an actual mp3 file
		f.write(requests.get(mp3URL).content)
	return mp3File

def generateTempFileName(extension):
	#generates a random file name with the intention of eventually deleting
	return "{}.{}".format(str(random.randint(99, 99999999)), extension)

def editMP3(mp3File):
	tempFile = generateTempFileName('mp3')
	#generates temporary mp3 file because FFMPEG will overwrite with -i param
	os.system("{} -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 -y -vol 1026 /tmp/{} && mv /tmp/{} {}".format(ffmpeg_bin, mp3File, tempFile, tempFile, mp3File))
	#this is the regular FFMPEG command to convert it to a playable audio file.  Notice the tmp and mv tmp.mp3, because -i will overwrite the file as you go along.

def generateSSML(text, region):
	url = generateURL(text, region.lower())
	#Gets URL from Google Translate
	mp3File = saveMP3(url, region)
	#Grabs mp3 from Google Translate and saves it locally
	editMP3(mp3File)
	#edits mp3 File to be the correct codec
	fileName = awsIntegration.uploadFile(mp3File)
	#uploads file to aws, returns AWS File name/location
	os.system('rm {}'.format(mp3File))
	# deletes file from local
	return fileName