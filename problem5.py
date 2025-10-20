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
		self.x = self.x + move
		if self.isWrapOn: 
			if self.x<0:
				self.x = self.__outputs - 1
			elif self.x> self.__outputs - 1:
				self.x = 0
		else:
			if self.x<0:
				self.x = 0
			elif self.x > self.__outputs - 1:
				self.x = self.__outputs - 1

			
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
