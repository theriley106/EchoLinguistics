'''
You should add some way to check that the file is valid
You should convert that mp3List.txt to JSON that contains file location
'''



import json
import os
import echoLinguistics
REDUCED_BANDWIDTH = True
#If this is set to False, it will regrab responses even if it's generated it before
TRIGGER_INTENT = 'saySomething'
#Name of intent on Alexa Skills Page
DEFAULT_TO_ALEXA = True
#Instead of throwing an error, it will return in Alexa's regular Voice if an error occurs
DB_FILE = "/tmp/mp3List.json"
#This is the file where all MP3 File Locations will be saved


def checkInFile(region):
	if REDUCED_BANDWIDTH == True:
		#Will only continue if you've set it to conserve bandwidth
		if os.path.exists(DB_FILE) == False:
			#Lambda only lets you save in /tmp/
			os.system("touch {}".format(DB_FILE))
			#creates DB_FILE if you don't have it already
		for previousAudio in json.load(open(DB_FILE)):
			#to reduce server costs, you can keep an updating list of responses to eliminate duplicate responses
			if region == previousAudio:
				return True
	return False

def saveResponse(text, region, fileLocation):
	#The expected input a SINGLE python dictionary object
	tempDict = {'Text': text, "Region": region, "fileLocation": fileLocation}
	with open(DB_FILE) as f:
	    data = json.load(f)
	#this is going to load a json file with the intention of "Cloning" and updating it
	data.update(tempDict)
	#Updates dict
	with open(DB_FILE, 'w') as f:
	    json.dump(data, f)
	#Dumps it to the same file
	
def on_intent(intent_request, session):
	intent = intent_request["intent"]
	intent_name = intent_request["intent"]["name"]
	# this is intent name you define in the Alexa Skills creators page
	if intent_name == TRIGGER_INTENT:
		languageChoice = intent['slots']['language']['value'].title()
		#This is the slot value that is picked when something is said to Alexa
		listOfLanguages = json.load(open("supportedLanguages.json"))
		regionChoice = next((item for item in listOfLanguages if item["Full_Name"] == languageChoice), None)
		#Region choice is a 2 letter region abbreviation.

		if checkInFile(region) == False:
			text = "I was successfully able to modify the Amazon Alexa voice.  Here it is speaking in a {} accent".format(abbr)
			fileLocation = echoLinguistics.generateSSML(text, regionChoice)
			# this invokes the function that makes the quote
			if REDUCED_BANDWIDTH == True:
				saveResponse(regionChoice)
		else:
			pass
			#What do you do if the file does exist???

		return genSSMLResponse(fileLocation)

	elif intent_name == 'aboutDev':
		return alexaHelper.devInfo()
	elif intent_name == "AMAZON.HelpIntent":
		return alexaHelper.get_help_response(REPEATSPEECH)
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return alexaHelper.handle_session_end_request()

def genSSMLResponse(fileLocation, shouldEndSession=True):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": 
			{
			      "type": "SSML",
			      "ssml": fileLocation
	    			},
					"shouldEndSession": shouldEndSession
				  }
		}

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


if __name__ == '__main__':
	on_intent({'intent': {'slots': {'language': {'value': 'Spanish'}}, 'name': 'saySomething'}, 'name': ''}, "")