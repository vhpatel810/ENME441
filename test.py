from shifter import Shifter
import time

s = Shifter(23,25,24)

try:
    while True:
        s.shiftByte(0b10101010)
        time.sleep(0.3)
        s.shiftByte(0b01010101)
        time.sleep(0.3)
except KeyboardInterrupt:
    pass
finally:
    s.shiftByte(0)
    GPIO.cleanup()
