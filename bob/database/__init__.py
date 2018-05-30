from peewee import *
import Event
import Iteration

# Database setup
db = SqliteDatabase('iterations.db')
db.connect()

if Iteration.table_exists() == False & Event.table_exists() == False:
  db.create_tables([Iteration, Event])