import time
import RPi.GPIO as GPIO

class Relay(object):
    def __init__(self, pin):
      self.pin = pin
      self.state = False
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(pin, GPIO.OUT)

    def off(self):
      if not self.state:
         return 
      GPIO.output(self.pin, GPIO.LOW) # out
      self.state = False

    def on(self):
      if self.state:
         return 
      GPIO.output(self.pin, GPIO.HIGH) # out
      self.state = True