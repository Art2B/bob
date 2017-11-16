# This file is useless for now. But it store scripts and stuff to display infos from the database. I'm gonna look for it later to make this better :)

itertationList = Iteration.select()
eventList = Event.select(Event, Iteration).join(Iteration)

for iteration in itertationList:
  print('Iteration number ' + str(iteration.number) + ". Begin at: " + str(iteration.begin_at))

for event in eventList:
  print("Event. Iteration number: " + str(event.iteration.number) + ". Date: " + str(event.date) + ". Text: " + str(event.text))