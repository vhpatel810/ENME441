import RPi.GPIO as GPIO
import time

class Shifter:
	def __init__(self, serialPin, clockPin, latchPin):
		self.serialPin = serialPin
		self.clockPin = clockPin
		self.latchPin = latchPin

		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.serialPin, GPIO.OUT)
		GPIO.setup(self.clockPin, GPIO.OUT, initial=0)
		GPIO.setup(self.latchPin, GPIO.OUT, initial=0)

	def __ping(self,p):
		GPIO.output(p,1)
		time.sleep(0)
		GPIO.output(p,0)

	def shiftByte(self,b):
		for i in range(8): 
			GPIO.output(self.serialPin, b & (1<<i) )
			self.__ping(self.clockPin)
		self.__ping(self.latchPin)
if __name__ == "__main__":
	try:
		shift = Shifter(23,25,24)
		shift.shiftByte(0b00000000)
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()


