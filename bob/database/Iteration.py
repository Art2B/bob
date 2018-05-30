class Iteration(Model):
  number = IntegerField()
  begin_at = DateTimeField()
  end_at = DateTimeField(null=True)
  colorCode = CharField(null=True)
  class Meta:
    database = db