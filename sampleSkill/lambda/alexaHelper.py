def returnSpeech(speech, endSession=True):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
		"outputSpeech": {
		"type": "PlainText",
		"text": speech
			},
			"shouldEndSession": endSession
		  }
		}

def devInfo():
	text = "created in February 2018 by Christopher Lambert.  This alexa skill is completely open sourced.  Please check out the skill on Git Hub or contact me for more information"
	return returnSpeech(text)

def get_welcome_response(skillName, initialSpeech, repeatSpeech):
	session_attributes = {}
	card_title = skillName
	speech_output = initialSpeech
	reprompt_text = repeatSpeech
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
	return {
		"version": "1.0",
		"sessionAttributes": session_attributes,
		"response": speechlet_response
	}

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

def get_help_response(helpText):
	return returnSpeech(helpText, False)

def handle_session_end_request(text="Exiting now..."):
	return {
	"version": "1.0",
	"sessionAttributes": {},
	"response": {
	"outputSpeech": {
	"type": "PlainText",
	"text": text
		},
		"shouldEndSession": True
	  }
	}
