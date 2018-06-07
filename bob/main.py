from gpiozero import Button
from signal import pause

from scheduled import Scheduler

print('Historian bob setting up.')
s = Scheduler()
button = Button(2)
button.when_released = s.start_new_world

print('Historian bob launched.')
s.start()
