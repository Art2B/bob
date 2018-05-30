from datetime import date, datetime
import json
import sched
import time
from TwitterAPI import TwitterAPI
from events import getEventFromYear
from peewee import *

# Open config file
with open('config.json', 'r') as f:
  config = json.load(f)

# Setup twitter api credentials
api = TwitterAPI(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"], config["twitter"]["access_token_key"], config["twitter"]["access_token_secret"])
# Set the current year
currentYear = date.today().year + 1

# Check if there is iterations in db and create one if not
if Iteration.select().count() == 0:
  print("Creating first iteration")
  Iteration(number=1, begin_at=datetime.now()).save()

def scheduledScript(sc, year):
  if year <= currentYear:
    event = getEventFromYear(year)
    currentIteration = Iteration.select().order_by(Iteration.begin_at.desc()).get()

    dbEvent = Event(
      iteration = currentIteration,
      date = event['date'],
      text = event['text']
    )
    # Tweet the event if localMode is false in config
    if config["main"]["localMode"] == False:
      r = api.request('statuses/update', {'status': event['text'][:config["twitter"]["maxChars"]]})
      dbEvent.tweet_id = r.json()['id_str']

    dbEvent.save()

    # Increment year for next iteration
    year = year + 1
    s.enter(config['main']['scFrequency'], 1, scheduledScript, (sc, year))
  else:
    print('End of this world iteration')
    currentIteration = Iteration.select().order_by(Iteration.begin_at.desc()).get()
    # Save end datetime of current iteration
    currentIteration.end_at = datetime.now()
    currentIteration.save()
    # Create new iteration
    newIterationNumber = currentIteration.number + 1
    Iteration(number=newIterationNumber, begin_at=datetime.now()).save()
    s.enter(config['main']['scFrequency'], 1, scheduledScript, (sc, config["main"]["startingYear"]))

# Retrieve starting year at launch and allow script to start where it stops
if Event.select().count() > 0:
  lastIteration = Iteration.select().order_by(Iteration.begin_at.desc()).get()
  lastEvent = Event.select(Event, Iteration).join(Iteration).where(Event.iteration == lastIteration).order_by(Event.date.desc()).get()
  startingYear = lastEvent.date.year + 1
else:
  startingYear = config["main"]["startingYear"]

s = sched.scheduler(time.time, time.sleep)
s.enter(config['main']['scFrequency'], 1, scheduledScript, (s, startingYear))
s.run()