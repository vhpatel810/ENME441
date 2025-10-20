import time
import random
from shifter import Shifter
import RPi.GPIO as GPIO

class Bug:
	def __init__(self,shifter:Shifter,timestep: float = 0.1, x: int = 3, isWrapOn: bool = False):
		self.x = x
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.__shifter = shifter

		self.__outputs = 8
		self.__wrap = False
	def __begin(self):
		self.__shifter.shiftByte(1<<self.x )
	def __steprandom(self):
		move = random.choice([-1,1])
		after = self.x + move
		if self.isWrapOn: 
			self.x = after % self.__outputs
		else:
			self.x = max(0,min(self.__outputs-1,after))
		self.__begin()
	def start(self):
		self.__wrap = True
		self.__begin()
	def stop(self):
		self.__wrap = False
		self.__shifter.shiftByte(0)
	def repeat(self):
		if not self.__wrap:
			return
		self.__steprandom()
		time.sleep(self.timestep)
if __name__ == "__main__":
    import RPi.GPIO as GPIO
    try:
        sh = Shifter(23, 25, 24)        # adjust pins if yours differ
        bug = Bug(sh, timestep=0.05, x=4, isWrapOn=False)
        bug.start()
        while True:
            bug.repeat()                # one step + sleep
    except KeyboardInterrupt:
        pass
    finally:
        try: bug.stop()
        except: pass
        GPIO.cleanup()

