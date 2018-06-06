from gpiozero import Button
from signal import pause

from scheduled import Scheduler

button = Button(2)

s = Scheduler()
s.start()

button.when_pressed = s.start_new_world 
pause()
