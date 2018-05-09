import requests
import bs4
import os

URL = "http://cache-a.oddcast.com/c_fs/4.mp3?engine=4&language=1&voice=11&text={0}&useUTF8=1"

def saveMP3(mp3URL, fileName):
	#return MP3 file name
	mp3File = '{}'.format(fileName)
	#calls it a random file name to later delete
	with open(mp3File, 'wb') as f:
		#this saves the response locally as an actual mp3 file
		f.write(requests.get(mp3URL).content)
	return mp3File

def genURL(text):
	# Returns the url containing an mp3 file for the inputted text
	text = text.replace(" ", "%20")
	# Converts to valid url text
	return URL.format(text)

def genVoice(text, success=True):
	# Generates the complete siri voice
	url = genURL(text)
	# Url for the voice only
	filename = saveMP3(url, 'testing.mp3')
	# Local file name
	combineFiles(filename, 'soundEffects/successCommand.mp3', 'final.mp3')

def combineFiles(file1, file2, saveAs):
	# Combines two mp3 files
	os.system('ffmpeg -i "concat:{}|{}" -acodec copy {}'.format(file1, file2, saveAs))
	# Combines two mp3 files to create a single file

if __name__ == '__main__':
	print genVoice(raw_input("Text: "))
