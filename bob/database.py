from datetime import datetime
from peewee import *

proxy = Proxy()

class Iteration(Model):
    number = IntegerField()
    begin_at = DateTimeField()
    end_at = DateTimeField(null=True)
    colorCode = CharField(null=True)
    class Meta:
        database = proxy

class Event(Model):
    iteration = ForeignKeyField(Iteration, related_name = 'events')
    date = DateTimeField()
    text = TextField()
    tweet_id = CharField(null=True)
    class Meta:
        database = proxy

def add_event(iteration, date, text, tweet_id):
    with proxy.atomic() as txn:
        Event.create(
            iteration = iteration,
            date = date,
            text = text,
            tweet_id = tweet_id
        ).save()

def add_iteration(number, begin_date):
    with proxy.atomic() as txn:
        Iteration.create(
            number = number,
            begin_at = begin_date,
        ).save()

def get_current_iteration():
    with proxy.atomic() as txn:
        return Iteration.select() \
                .order_by(Iteration.begin_at.desc()) \
                .get()

def get_last_event():
    with proxy.atomic() as txn:
        current_iteration = get_current_iteration()
        return Event.select(Event, Iteration) \
                .join(Iteration) \
                .where(Event.iteration == current_iteration) \
                .order_by(Event.date.desc()) \
                .get() \

def create_new_iteration():
    currentIteration = get_current_iteration()
    # Save end datetime of current iteration
    currentIteration.end_at = datetime.now()
    currentIteration.save()
    # Create new iteration
    # Find a more elegant way to do this with database configuration :)
    newIterationNumber = currentIteration.number + 1
    add_iteration(newIterationNumber, datetime.now())