import random
import time
from shifter import Shifter
import RPi.GPIO as GPIO

shift = Shifter(23,25,24)
x = 4
outputs =8
try:
	while True:
		shift.shiftByte(1<<x)
		move = random.choice([-1,1])
		x += move
		if x < 0: 
			x=0
		elif x>= outputs:
			x = outputs-1
		time.sleep(0.05)
except KeyboardInterrupt:
	GPIO.cleanup()


