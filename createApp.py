import json
var = ""
listOfLanguages = json.load(open("supportedLanguages.json"))
listOfLanguage = []
for item in listOfLanguages:
	if item["Full_Name"] not in listOfLanguage:
		listOfLanguage.append(item['Full_Name'])
		var = var + """
			{{
							"id": null,
							"name": {{
								"value": "{Full_Name}",
								"synonyms": [
									"{Abbreviation}"
								]
							}}
						}},
						""".format(**item)
with open("hello.txt", "w") as f:
	f.write(var)