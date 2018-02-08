import requests
import bs4


def grabSite(url):
	return requests.get(url, headers=headers)




def translate(text="", toLanguage="Es", fromLanguage='En'):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.session()
	url = 'https://translate.google.com/#{}/{}/'.format(fromLanguage, toLanguage)
	rez = res.get(url, headers=headers)
	f = res.get("https://translate.google.com/translate_a/single?client=t&sl=en&tl=es&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&swap=1&ssel=5&tsel=5&kc=1&q=Test%20to%20see%20if%20this%20works")
	print f.json()
	page = bs4.BeautifulSoup(rez.text, 'lxml')
	print page.title.string


translate()
