from googletrans import Translator


try:
	SECRET_KEY = open("secretKey.txt").read().strip()
	ACCESS_KEY = open("accessKey.txt").read().strip()
	tempBucketID = open("bucketID.txt").read().strip()
except:
	print("No security credentials set up")
	print("create secretCode.txt and accessKey.txt")
	raise Exception("No config files")

# This just confirms that you have all configuration files
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
	generateSSML(text, accentAbbreviation)
	# This is the function that generates the ssml audio object
	return returnSSMLResponse("{}.mp3".format(accentAbbreviation))
	# This is the python dict that the echo can interperet
