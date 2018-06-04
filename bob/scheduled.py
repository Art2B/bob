from datetime import date, datetime
import time
import sched
import json

import peewee as pw

from twitter import tweet
import database as db
from events import getEventFromYear

# Open config file
with open('config.json', 'r') as f:
    config = json.load(f)

class Scheduler:
    def __init__(self):
        # Database setup
        iterationDB = pw.SqliteDatabase('iterations.db')
        iterationDB.connect()
        db.proxy.initialize(iterationDB)
        iterationDB.create_tables([db.Iteration, db.Event], safe=True)

        # Check if there is iterations in db and create one if not
        if db.Iteration.select().count() == 0:
            db.add_iteration(1, datetime.now())

        # Set scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)

        # Set current year
        self.currentYear = date.today().year + 1

        # Retrieve starting year at launch and allow script to start where it stops
        if db.Event.select().count() > 0:
            lastEvent = db.get_last_event()
            self.startingYear = lastEvent.date.year + 1
        else:
            self.startingYear = config["main"]["startingYear"]

    def start():
        self.scheduler.enter(
            config['main']['scFrequency'],
            1,
            self.script,
            (self.scheduler, self.startingYear)
        )
        self.scheduler.run()

    def stop():
        # To write

    def script(sc, year):
        if year <= self.currentYear:
            event = getEventFromYear(year)
            currentIteration = db.get_current_iteration()
            tweet_id = tweet(event['text'])

            db.add_event(
                currentIteration,
                event['date'],
                event['text'],
                tweet_id
            )

            # Increment year for next iteration
            year = year + 1
            self.scheduler.enter(
                config['main']['scFrequency'],
                1,
                self.script,
                (sc, year)
            )
        else:
            print('End of this world iteration')
            db.create_new_iteration()
            s.enter(
                config['main']['scFrequency'],
                1,
                scheduledScript,
                (sc, config["main"]["startingYear"])
            )
