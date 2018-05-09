import requests
import bs4

URL = "http://cache-a.oddcast.com/c_fs/4.mp3?engine=4&language=1&voice=11&text={0}&useUTF8=1"

def genURL(text):
	# Returns the url containing an mp3 file for the inputted text
	text = text.replace(" ", "%20")
	# Converts to valid url text
	return URL.format(text)

if __name__ == '__main__':
	print genURL(raw_input("Text: "))
