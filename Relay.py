import RPi.GPIO as GPIO
import time

in1 = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.output(in1, False)

try:
    while True:
      for x in range(5):
            GPIO.output(in1, True)
            time.sleep(5)
            GPIO.output(in1, False)
            time.sleep(5)
      
      GPIO.output(in1,True)

      for x in range(4):
            GPIO.output(in1, True)
            time.sleep(2)
            GPIO.output(in1, False)
            time.sleep(2)
      GPIO.output(in1,True)

except KeyboardInterrupt:
    GPIO.cleanup()