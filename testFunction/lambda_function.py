from boto3 import client as botoClient
import json
import os
from googletrans import Translator
lambdas = botoClient("lambda", region_name='us-east-1')
GREETING_MESSAGE = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
# This is the message alexa will say when starting the skill
GREETING_MESSAGE2 = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
# This is the message alexa will say after leaving the skill open for ~10 seconds
TEXT_TO_SAY = "I was successfully able to modify the Amazon Alexa voice.  Here it is speaking {0} in a {1} accent"
SSML_URL = "https://s3.amazonaws.com/nucilohackathonbucket/{0}"
# This is the url of the S3 Bucket - make sure this is a publicly available bucket.
DB_FILE = '/tmp/mp3List.txt'
# This is the file where the previously generated file information is stored

def checkInFile(region):
	for val in open(DB_FILE).read().split("\n"):
		if region == val:
			return True
	return False

def genSSML(fileName):
	return SSML_URL.format(fileName)

def translateText(text, toLanguage, fromLanguage="en"):
	translator = Translator()
	translation = translator.translate(text, dest=toLanguage)
	return translation.text

def getListOfLanguages(languageList='supportedLanguages.json'):
	return json.load(open("supportedLanguages.json"))

def createmp3List():
	if os.path.exists(DB_FILE) == False:
		os.system("touch {}".format(DB_FILE))

def returnLanguageAbbrFromFull(fullLanguage):
	for value in getListOfLanguages():
		#value type = dict
		if fullLanguage == value["Full_Name"]:
			#the language that the user
			return value["Abbreviation"].lower()

def generateText(language, accent, languageAbbreviation):
	if languageAbbreviation != "en":
			return translateText(TEXT_TO_SAY.format(language, accent), languageAbbreviation)
	else:
		return TEXT_TO_SAY.format(language, accent)

def genPayload(text, accentAbbreviation):
	return json.dumps({
			  "Text": text,
			  "Region": accentAbbreviation
			})

def returnSSMLResponse(ssmlFile, endSession=True):
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
	try:
		language = intent['slots']['language']['value']
		#Trys to find out if the language is defined
	except:
		language = "English"
		#else defaults as English
	languageAbbreviation = returnLanguageAbbrFromFull(language)
	#Defines the abbreviated version of the language sent in the request
	accent = intent['slots']['accentVal']['value']
	# defines the accent language
	accentAbbreviation = returnLanguageAbbrFromFull(accent)
	# returns accent abbreviation
	text = generateText(language, accent, languageAbbreviation)
	# generate text that gets returned
	print("tell me something in {} in a {} accent".format(language, accent))
	#purely for debug reasons
	lambdas.invoke(FunctionName="ffmpegLambda", InvocationType="RequestResponse", Payload=genPayload(text, accentAbbreviation))
	# This is the lambda function that generates the ssml object
	return returnSSMLResponse("{}.mp3".format(accentAbbreviation))
	# This is the python dict that the echo can interperet

def returnLanguageSlotValue(intent, default="Spanish"):
	try:
		return intent['slots']['language']['value'].title()
	except:
		return default



def on_intent(intent_request, session):
	intent = intent_request["intent"]
	intent_name = intent_request["intent"]["name"]
	if intent_name == 'useAccent':
		return genAccentSSML(intent)
		# This generates the valid response that is sent to the echo

	if intent_name == 'saySomething':
		languageName = returnLanguageSlotValue(intent)
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

	elif intent_name == 'aboutDev':
		return alexaHelper.devInfo()
	elif intent_name == "AMAZON.HelpIntent":
		return alexaHelper.get_help_response(REPEATSPEECH)
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return alexaHelper.handle_session_end_request()

def on_launch(launch_request, session):
	return get_welcome_response()

def get_welcome_response():
	session_attributes = {}
	card_title = "Transit Tracker"
	speech_output = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
	reprompt_text = "Modifying Amazon Echo Speech using speech synthesis markup language by Christopher Lambert"
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
	output = "Please ask me to generate a scramble.  You can also ask about the Developer of this application.  What can I help you with?"
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
	"text": "Thanks for checking out Rubiks Scrambler!"
		},
		"shouldEndSession": True
	  }
	}

createmp3List()
if __name__ == '__main__':
	on_intent({'intent': {'slots': {'language': {'value': 'Spanish'}}, 'name': 'saySomething'}, 'name': ''}, "")
