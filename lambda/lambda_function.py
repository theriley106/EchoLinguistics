import json
import os
from googletrans import Translator
import os
import re
import shutil
import sys
import requests
import random
import json
import tinys3
import time

try:
	SECRET_KEY = open("secretCode.txt").read().strip()
	ACCESS_KEY = open("accessKey.txt").read().strip()
except:
	print("No security credentials set up")
	print("create secretCode.txt and accessKey.txt")

# This just confirms that you have all configuration files
FFMPEG_FILE_LOCATION = "/tmp/ffmpeg.linux64"
# /tmp/ is the only lambda folder you have r/w access to
shutil.copyfile('/var/task/ffmpeg.linux64', FFMPEG_FILE_LOCATION)
# This copies the files in /var/task/ffmpeg.linux64 on every lambda run
os.chmod(FFMPEG_FILE_LOCATION, os.stat(FFMPEG_FILE_LOCATION).st_mode | stat.S_IEXEC)
# This makes that ffmpeg file executable
lambdas = botoClient("lambda", region_name='us-east-1')
# This opens up a botoClient to interact with the ffmpeg lambda function
SKILL_NAME = "Echo Linguistics"
# This is also the card title
GREETING_MESSAGE = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
# This is the message alexa will say when starting the skill
GREETING_MESSAGE2 = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
# This is the message alexa will say after leaving the skill open for ~10 seconds
TEXT_TO_SAY = "I was successfully able to modify the Amazon Alexa voice.  Here it is speaking {0} in a {1} accent"
# This is the text that the third party voice will say
HELP_RESPONSE = "You can tell me to speak different languages or speak in different accents"
# This is the response that is said when a user asks alexa for help using the skill
END_RESPONSE = "Thank you for checking out Echo Linguistics"
# This is the end request text that is sent when the client exits to skill
SSML_URL = "https://s3.amazonaws.com/nucilohackathonbucket/{0}"
# This is the url of the S3 Bucket - make sure this is a publicly available bucket.
DB_FILE = '/tmp/mp3List.txt'
# This is the file where the previously generated file information is stored
LOW_BANDWIDTH = True
# This tells the skill whether or not to regrab duplicate files
LANGUAGE_LIST = json.loads(open("supportedLanguages.json").read())
# This contains all supported languages

def uploadFile(fileName):
	bucketID = extractBucketID(SSML_URL)
	finalFileName = fileName.split('/')[-1]
	conn = tinys3.Connection(ACCESS_KEY,SECRET_KEY,tls=True)
	conn.upload(finalFileName, open(fileName,'rb'), bucketID)
	return "<speak><audio src='https://s3.amazonaws.com/{}/{}'/></speak>".format(bucketID, fileName)

def editMP3(mp3File):
	# Makes the generated mp3File work on the Echo
	os.system("{} -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 -y -vol 1026 /tmp/tmp.mp3 && mv /tmp/tmp.mp3 {}".format(FFMPEG_FILE_LOCATION, mp3File, mp3File))
	#this is the regular FFMPEG command to convert it to a playable audio file.  Notice the tmp and mv tmp.mp3, because -i will overwrite the file as you go along.

def extractBucketID(ssmlValue):
	# This just converts the ssml value into a bucket ID for uploadFile
	return ssmlValue.partition(".com/")[2].partition("/")[0]

def checkInFile(region):
	# This checks to see if the region is in the file exists already
	for val in open(DB_FILE).read().split("\n"):
		# This checks to see if the line in the file matches the region
		if region == val:
			return True
	return False

def generateSSML(text, region=None):
	if region == None:
		region = random.choice(LANGUAGE_LIST)['Abbreviation']
	url = generateURL(text, region.lower())
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

def generateURL(keyWords, region):
	# This generates the GOOGLE TRANSLATE URL
	keyWords = keyWords.replace(" ", "%20")
	# Google translate url doesn't have a space
	return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}".format(keyWords, region)

def genSSML(fileName):
	return SSML_URL.format(fileName)

def translateText(text, toLanguage, fromLanguage="en"):
	# This translates text into the language described in fromLanguage
	translator = Translator()
	# Initiates translator class
	translation = translator.translate(text, dest=toLanguage)
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

def generateText(language, accent, languageAbbreviation):
	if languageAbbreviation != "en":
		# This simply means the text needs to be translated
			return translateText(TEXT_TO_SAY.format(language, accent), languageAbbreviation)
	else:
		# This means it is going from en to en so no translation is required
		return TEXT_TO_SAY.format(language, accent)

def genPayload(text, accentAbbreviation):
	# This is the payload that is sent to the lambda function
	return json.dumps({
			  "Text": text,
			  "Region": accentAbbreviation
			})

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

def genAccentSSML(intent):
	languageName = returnLanguageSlotValue(intent, default="English")
	# Full name of the language sent in the request: ie, English, Spanish, etc.
	languageAbbreviation = returnLanguageAbbrFromFull(languageName)
	#Defines the abbreviated version of the language sent in the request
	accentVal = intent['slots']['accentVal']['value']
	# defines the accent language
	accentAbbreviation = returnLanguageAbbrFromFull(accentVal)
	# returns accent abbreviation
	text = generateText(languageName, accentVal, languageAbbreviation)
	# generate text that gets returned
	print("tell me something in {} in a {} accent".format(languageName, accentVal))
	#purely for debug reasons
	lambdas.invoke(FunctionName="ffmpegLambda", InvocationType="RequestResponse", Payload=genPayload(text, accentAbbreviation))
	# This is the lambda function that generates the ssml object
	return returnSSMLResponse("{}.mp3".format(accentAbbreviation))
	# This is the python dict that the echo can interperet

def returnLanguageSlotValue(intent, default="Spanish"):
	# This tells the developer the slot values that the client said
	try:
		return intent['slots']['language']['value'].title()
	except:
		# This means that the user didn't fill any language slots in their request
		return default

def genSaySomethingSSML(intent):
	languageName = returnLanguageSlotValue(intent)
	# Full name of the language sent in the request: ie, English, Spanish, etc.
	languageAbbreviation = returnLanguageAbbrFromFull(languageName)
	# this should be a lower case abbreviation: ie. es or en | languageAbbreviation is also accent for this intent
	text = generateText(languageName, languageName, languageAbbreviation)
	#This generates the text that the alexa says - it will translate from the english in TEXT_TO_SAY
	if checkInFile(region) == False:
		#This checks to see if you have already created this file before
		lambdas.invoke(FunctionName="ffmpegLambda", InvocationType="RequestResponse", Payload=genPayload(text, languageAbbreviation))
		# this invokes the lambda function that makes the quote
		with open(DB_FILE, 'a') as file:
			#This saves it so that it knows to use this file in the future
			file.write('{}\n'.format(region))
			# You could probably use os.system("echo {} >> {}".format(region, DB_FILE)) here
	return returnSSMLResponse("{}.mp3".format(languageAbbreviation))


def on_intent(intent_request, session):
	intent = intent_request["intent"]
	# This is all of the info regarding the intent'
	intent_name = intent_request["intent"]["name"]
	# This is specifically the name of the intent you created

	if intent_name == 'useAccent':
		# alexa say something in german with a spanish accent
		return genAccentSSML(intent)
		# This generates the valid response that is sent to the echo

	if intent_name == 'saySomething':
		# alexa say something in german
		return genSaySomethingSSML(intent)
		# This is the function that says something without modifying accent

	elif intent_name == 'aboutDev':
		# Alexa tell me about the developer
		return alexaHelper.devInfo()

	elif intent_name == "AMAZON.HelpIntent":
		# Alexa help
		return alexaHelper.get_help_response(REPEATSPEECH)

	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		# Alexa stop / Alexa cancel
		return alexaHelper.handle_session_end_request()

def on_launch(launch_request, session):
	# As soon as the application is loaded
	return get_welcome_response()

def get_welcome_response():
	session_attributes = {}
	card_title = SKILL_NAME
	speech_output = GREETING_MESSAGE
	reprompt_text = GREETING_MESSAGE2
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def lambda_handler(event, context):
	if event["request"]["type"] == "LaunchRequest":
		return on_launch(event["request"], event["session"])
	elif event["request"]["type"] == "IntentRequest":
		return on_intent(event["request"], event["session"])
	else:
		handle_session_end_request()

def get_help_response():
	output = HELP_RESPONSE
	return returnSpeech(output, False)

def build_speechlet_response(title, output, reprompt_text, should_end_session):
	return {
		"outputSpeech": {
			"type": "PlainText",
			"text": output
		},
		"card": {
			"type": "Simple",
			"title": title,
			"content": output
		},
		"reprompt": {
			"outputSpeech": {
				"type": "PlainText",
				"text": reprompt_text
			}
		},
		"shouldEndSession": should_end_session
	}

def build_response(session_attributes, speechlet_response):
	return {
		"version": "1.0",
		"sessionAttributes": session_attributes,
		"response": speechlet_response
	}

def handle_session_end_request():
	return {
	"version": "1.0",
	"sessionAttributes": {},
	"response": {
	"outputSpeech": {
	"type": "PlainText",
	"text": END_RESPONSE
		},
		"shouldEndSession": True
	  }
	}

createmp3List()
if __name__ == '__main__':
	on_intent({'intent': {'slots': {'language': {'value': 'Spanish'}}, 'name': 'saySomething'}, 'name': ''}, "")
