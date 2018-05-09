from googletrans import Translator
# This is used for tranlating the text
import json
# This is primarily used for using the supported language list
import shutil
# This is used to copy ffmpeg to executable path
import random
# This is used for picking a random language when it's not specified
import stat
# This is used to make ffmpeg executable
import requests
# This is used to grab/save the mp3 file from google
import os
# This is for granting ffmpeg executable permissions
import tinys3
# This is for uploading files to s3
import re
# This is for grabbing the mp3 names from the val character
import siriVoice
# Import the voice for Siri

'''
Format of DB
I was successfully able to modify the Amazon Alexa voice.  Here it is speaking german in a spanish accent | de_es_11.mp3
I was successfully able to modify the Amazon Alexa voice.  Here it is speaking korean in a spanish accent | ko_es_12.mp3
'''

try:
	SECRET_KEY = open("secretKey.txt").read().strip()
	# This is the AWS Secret key for interacting with the S3 bucket
	ACCESS_KEY = open("accessKey.txt").read().strip()
	# This is the AWS Access key for interacting with the S3 bucket
	tempBucketID = open("bucketID.txt").read().strip()
	# This is the "Temp" bucketID that is eventually used to create SSML_URL
except:
	print("No security credentials set up")
	print("create secretCode.txt and accessKey.txt")
	raise Exception("No config files")
	# Please follow instructions in readme if you keep getting this error
# ^ This just confirms that you have all configuration files

FFMPEG_FILE_LOCATION = "/tmp/ffmpeg.linux64"
# /tmp/ is the only lambda folder you have r/w access to
shutil.copyfile('/var/task/ffmpeg.linux64', FFMPEG_FILE_LOCATION)
# This copies the files in /var/task/ffmpeg.linux64 on every lambda run
os.chmod(FFMPEG_FILE_LOCATION, os.stat(FFMPEG_FILE_LOCATION).st_mode | stat.S_IEXEC)
# This makes that ffmpeg file executable
SSML_URL = tempBucketID + "{0}"
# This is the url of the S3 Bucket - make sure this is a publicly available bucket.
DB_FILE = '/tmp/mp3List.txt'
# This is the file where the previously generated file information is stored
LOW_BANDWIDTH = True
# This tells the skill whether or not to regrab duplicate files
LANGUAGE_LIST = json.loads(open("supportedLanguages.json").read())
# This contains all supported languages
FILENAME_FORMAT = "{0}_{1}_{2}.mp3"
# 0 = Language; 1 = Accent; 2 = Index in txt file


########### Function declarations  ###########################

def returnSSMLResponse(ssmlFile, endSession=True):
	# This is the full *completed* response that's sent to the client
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech":
			{
			      "type": "SSML",
			      "ssml": "<speak><audio src='{}'/></speak>".format(SSML_URL.format(ssmlFile))
	    			},
					"shouldEndSession": endSession
				  }
		}

def uploadFile(fileName):
	bucketID = extractBucketID(SSML_URL)
	# This converts the bucketID from "https://s3.amazonaws.com/bucketid/" to "bucketid"
	finalFileName = fileName.split('/')[-1]
	# Converts the input from /whateverinput/ to whateverinput
	conn = tinys3.Connection(ACCESS_KEY,SECRET_KEY,tls=True)
	# This open up the s3 conneciton using the constants defined at the beginning
	# TODO - Ideally this would be a class that would take these vars on input and test...
	conn.upload(finalFileName, open(fileName,'rb'), bucketID)
	# This uploads that
	return "<speak><audio src='https://s3.amazonaws.com/{}/{}'/></speak>".format(bucketID, fileName)
	# This is the format the echo can use

def findHighestIndex():
	# This returns the highest file number saved in the DB
	try:
		fileName = re.findall("\S+\.mp3", str(open(DB_FILE).read()))[-1]
		# Regex all mp3 files in that string of text
		indexNum = re.findall('\d+', fileName)[0]
		# Returns all digits, and picks the first one which is the index number
	except Exception as exp:
		indexNum = 0
		# Defaults to 0 if the file was just created
	return int(indexNum)

def writeToDB(text, language, accent):
	# Writes the filename to the database defined in DB_FILE
	indexNum = findHighestIndex() + 1
	# This generates the index number the text will use
	os.system('echo "{} | {}_{}_{}.mp3" >> {}'.format(text, language, accent, indexNum, DB_FILE))

def editMP3(mp3File):
	# Makes the generated mp3File work on the Echo
	os.system("{} -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 -y -vol 1026 /tmp/tmp.mp3 && mv /tmp/tmp.mp3 {}".format(FFMPEG_FILE_LOCATION, mp3File, mp3File))
	#this is the regular FFMPEG command to convert it to a playable audio file.  Notice the tmp and mv tmp.mp3, because -i will overwrite the file as you go along.

def extractBucketID(ssmlValue):
	# This just converts the ssml value into a bucket ID for uploadFile
	return ssmlValue.partition(".com/")[2].partition("/")[0]

def checkInFile(string):
	# This checks to see if audio has been created with this string
	for val in open(DB_FILE).read().split("\n"):
		# This checks to see if the line in the file matches the region
		if '|' in str(val):
			if string == str(val).partition("|")[0].strip():
				return True
	return False

def findIndex(string, accent, toLanguage):
	for val in open(DB_FILE).read().split("\n"):
		# This checks to see if the line in the file matches the region
		if '|' in str(val):
			if string == str(val).partition("|")[0].strip():
				fileName = re.findall("\S+\.mp3", str(val))[0]
				if fileName.split('_')[0] == toLanguage and fileName.split("_")[1] == accent:
					return fileName

def generateSSML(text, fileName, region=None):
	if region == None:
		# This means the user didn't define the region in the utterance
		region = random.choice(LANGUAGE_LIST)['Abbreviation']
		# Just picks a random region from the language list
	url = generateURL(text, region.lower())
	# Returns in the format of https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=...
	mp3File = saveMP3(url, fileName)
	# This grabs the mp3 file using requests | the region is the file name...
	editMP3(mp3File)
	# This doesn't return anything.  TO DO: Maybe a better way of doing this(?)
	rawSSML = uploadFile(mp3File)
	# This is raw SSML.  Ie: <speak><audio src='...
	os.system('rm {}'.format(mp3File))
	# Removes the mp3 File from the lambda function
	print("Successfully downloaded")
	# TODO: Maybe add a verbose == True(?)
	return rawSSML

def genFileName(text, accent, language):
	indexNum = findHighestIndex() + 1
	return '{}_{}_{}.mp3'.format(language, accent, indexNum)

def saveMP3(mp3URL, fileName):
	#return MP3 file name
	mp3File = '/tmp/{}'.format(fileName)
	#calls it a random file name to later delete
	with open(mp3File, 'wb') as f:
		#this saves the response locally as an actual mp3 file
		f.write(requests.get(mp3URL).content)
	return mp3File

def generateURL(keyWords, region):
	# This generates the GOOGLE TRANSLATE URL
	keyWords = keyWords.replace(" ", "%20")
	# Google translate url doesn't have a space
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}".format(keyWords, region)

def translateText(text, toLanguage, fromLanguage="en"):
	# This translates text into the language described in fromLanguage
	translator = Translator()
	# Initiates translator class
	translation = translator.translate(text, dest=toLanguage, src=fromLanguage)
	# .to_dict or .text work with this object
	return translation.text

def getListOfLanguages(languageList='supportedLanguages.json'):
	# This contains all supported languages
	return json.load(open("supportedLanguages.json"))

def createmp3List():
	# This "creates" mp3List if it doesn't exist already.
	if os.path.exists(DB_FILE) == False:
		# The file doesn't exist
		os.system("touch {}".format(DB_FILE))
		# Create the file

def returnLanguageAbbrFromFull(fullLanguage):
	for value in getListOfLanguages():
		#value type = dict
		if fullLanguage == value["Full_Name"]:
			#the language that the user
			return value["Abbreviation"].lower()

def speak(text, accent=None, fromLanguage="en", toLanguage="en", fileName=None, siri=False):
	if siri == False:
		if toLanguage != "en":
			# This means you want to translate the text
			text = translateText(text, toLanguage, fromLanguage)
			# Input: text | Output: text
		if accent == None:
			accent = toLanguage
		if LOW_BANDWIDTH == True:
			if checkInFile(text) == True:
				fileName = findIndex(text, accent, toLanguage)
		if fileName == None:
			# If the file name doesn't exist it will make it
			fileName = genFileName(text, accent, toLanguage)
			# This generates the filename of the speach file.  ie "en_es_111.mp3"
			generateSSML(text, fileName, accent)
			# This is the function that generates the ssml audio object
			if LOW_BANDWIDTH == True:
				# You can disable this by setting LOW_BANDWIDTH to False
				writeToDB(text, toLanguage, accent)
				# This saves the file in a DB to save bandwidth
		return returnSSMLResponse(fileName)
		# This is the python dict that the echo can interperet
	else:
		url = siriVoice.genURL(text)
		# This generates the URL for the siri voice file
		fileName = 'siritest.mp3'
		# Filename for the siri voice file
		mp3File = saveMP3(url, fileName)
		# This grabs the mp3 file using requests | the region is the file name...
		editMP3(mp3File)
		# This doesn't return anything.  TO DO: Maybe a better way of doing this(?)
		rawSSML = uploadFile(mp3File)
		# This is raw SSML.  Ie: <speak><audio src='...
		os.system('rm {}'.format(mp3File))
		# Removes the mp3 File from the lambda function
		print("Successfully downloaded")
		# TODO: Maybe add a verbose == True(?)
		return returnSSMLResponse(fileName)
		# This is the python dict that the echo can interperet

######### This runs anytime echoLinguistics.py is imported  #######################
createmp3List()
# This creates the list of mp3 files that have already been generated
