from datetime import date, datetime
import json
import sched
import time

import peewee as pw
from TwitterAPI import TwitterAPI

from events import getEventFromYear
import database as db

# Open config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Setup twitter api credentials
api = TwitterAPI(
    config["twitter"]["consumer_key"],
    config["twitter"]["consumer_secret"],
    config["twitter"]["access_token_key"],
    config["twitter"]["access_token_secret"]
)

# Database setup
iterationDB = pw.SqliteDatabase('iterations.db')
iterationDB.connect()
db.proxy.initialize(iterationDB)
iterationDB.create_tables([db.Iteration, db.Event], safe=True)

# Set the current year
currentYear = date.today().year + 1

# Check if there is iterations in db and create one if not
if db.Iteration.select().count() == 0:
    db.add_iteration(1, datetime.now())

def scheduledScript(sc, year):
    if year <= currentYear:
        event = getEventFromYear(year)
        currentIteration = db.get_current_iteration()

        tweet_id = None

        # Tweet the event if localMode is false in config
        if config["main"]["localMode"] == False:
            r = api.request(
                'statuses/update',
                {
                    'status': event['text'][:config["twitter"]["maxChars"]]
                }
            )
            tweet_id = r.json()['id_str']

        db.add_event(
            currentIteration,
            event['date'],
            event['text'],
            tweet_id
        )

        # Increment year for next iteration
        year = year + 1
        s.enter(
            config['main']['scFrequency'],
            1,
            scheduledScript,
            (sc, year)
        )
    else:
        print('End of this world iteration')
        currentIteration = db.get_current_iteration()

        # Save end datetime of current iteration
        currentIteration.end_at = datetime.now()
        currentIteration.save()
        # Create new iteration
        # Find a more elegant way to do this with database configuration :)
        newIterationNumber = currentIteration.number + 1
        db.add_iteration(newIterationNumber, datetime.now())
        s.enter(
            config['main']['scFrequency'],
            1,
            scheduledScript,
            (sc, config["main"]["startingYear"])
        )

# Retrieve starting year at launch and allow script to start where it stops
if db.Event.select().count() > 0:
    lastIteration = db.get_current_iteration()
    lastEvent = db.get_last_event()
    startingYear = lastEvent.date.year + 1
else:
    startingYear = config["main"]["startingYear"]

s = sched.scheduler(time.time, time.sleep)
s.enter(config['main']['scFrequency'], 1, scheduledScript, (s, startingYear))
s.run()