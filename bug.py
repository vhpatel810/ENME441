import RPi.GPIO as GPIO 
from shifter import Shifter
from problem5 import Bug

S1 = 17
S2 =27
S3 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(S1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(S2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(S3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	shift = Shifter(23,25,24)
	timedefault = 0.10
	bug = Bug(shift, timestep = timedefault, x = 4, isWrapON= False)
	laststate = GPIO.input(S2)
	while True: 
		if GPIO.input(S1) == GPIO.LOW:
			bug.start()
		else: 
			bug.stop()
	current_s2 = GPIO.input(S2)
	if laststate == GPIO.HIGH and current_s2 ==GPIO.LOW:
		bug.isWrapOn = not bug.isWrapON
	laststate = current_s2

	bug.timestep= (timedefault/3) if (GPIO.input (S3)== GPIO.LOW else timedefault
	bug.repeat()
except KeyboardInterrupt:
	GPIO.cleanup()
