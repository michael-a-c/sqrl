import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 23
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
print(1)
time.sleep(2)
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
print(2)
time.sleep(2)
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
print(3)