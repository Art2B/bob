from datetime import datetime
import requests
import json
import re

wikiEndpoint = "https://en.wikipedia.org/w/api.php"

logFile = open("result.log", "r")

year = 1932
currentYear = datetime.now().year

# Get data here
r = requests.get(wikiEndpoint + "?action=query&prop=revisions&rvprop=content&format=json&titles=" + str(year))
data = json.loads(r.text)['query']['pages']
data = data[next(iter(data))]['revisions'][0]['*']