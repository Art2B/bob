from datetime import date, datetime
import time
import sched

import peewee as pw

from twitter import tweet
import database as db
from events import getEventFromYear
from config import get as get_config
from helpers import get_explosion_gif

config = get_config()

class Scheduler:
    def __init__(self):
        # Database setup
        iterationDB = pw.SqliteDatabase('bob.db')
        iterationDB.connect()
        db.proxy.initialize(iterationDB)
        iterationDB.create_tables([db.Iteration, db.Event], safe=True)

        # Check if there is iterations in db and create one if not
        if db.Iteration.select().count() == 0:
            db.add_iteration(1, datetime.now())

        self.reset()

    def start(self, year = None):
        self.scheduler.enter(
            config['main']['scFrequency'],
            1,
            self.script,
            (self.scheduler, year or self.startingYear)
        )
        self.scheduler.run()

    def reset(self):
        # Set scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.currentYear = date.today().year + 1

        if db.get_events_number_for_iteration() > 0:
            lastEvent = db.get_last_event()
            self.startingYear = lastEvent.date.year + 1
        else:
            self.startingYear = config['main']['startingYear']


    def start_new_world(self):
        # End current iteration
        db.create_new_iteration()
        self.reset()
        current_iteration = db.get_current_iteration()
        # Get explosion gif
        gif = get_explosion_gif()
        # Tweet about end of world
        tweet('World\'s destruction initiated.')
        tweet('3.')
        tweet('2.')
        tweet('1.')
        tweet('Booom ! ' + gif['url'])
        tweet('Generating new world.')
        tweet('World #' + str(current_iteration.number) + ' operational.')
        # start again
        self.start()

    def script(self, sc, year):
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
            self.start(year + 1)
        else:
            # End of this world iteration
            db.create_new_iteration()
            tweet('World is over.')
            tweet('Generating new world.')
            tweet('World #' + str(current_iteration.number) + ' operational.')
            self.start()
