from datetime import date
import json
import sched
import time
from TwitterAPI import TwitterAPI
from events import getEventFromYear

with open('config.json', 'r') as f:
  config = json.load(f)

api = TwitterAPI(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"], config["twitter"]["access_token_key"], config["twitter"]["access_token_secret"])
currentYear = date.today().year + 1

def scheduledScript(sc, year):
  if year <= currentYear:
    event = getEventFromYear(year)
    print(event)
    if config["main"]["localMode"] == False:
      r = api.request('statuses/update', {'status': event[:config["twitter"]["maxChars"]]})
    year = year + 1
    s.enter(config['main']['scFrequency'], 1, scheduledScript, (sc, year))  
  else:
    print('End of this world iteration')

s = sched.scheduler(time.time, time.sleep)
s.enter(config['main']['scFrequency'], 1, scheduledScript, (s, config["main"]["startingYear"]))
s.run()