import time
import RPi.GPIO as GPIO

class Relay(object):
    def __init__(self, pin):
      self.pin = pin
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(pin, GPIO.OUT)

    def off(self):
      GPIO.output(self.pin, GPIO.LOW) # out

    def on(self):
      GPIO.output(self.pin, GPIO.HIGH) # out
