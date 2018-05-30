class Event(Model):
  iteration = ForeignKeyField(Iteration, related_name='events')
  date = DateTimeField()
  text = TextField()
  tweet_id = CharField(null=True)
  class Meta:
    database = db