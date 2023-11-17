import pigpio
import time
servo_min = 500  # Minimum pulse width
servo_max = 2500  # Maximum pulse width

class ServoController(object):
    def __init__(self, pin):
        self.pin = pin
        self.pi = pigpio.pi()
        self.angle = 0
 
# Function to move the servo to a specific angle
    def set_angle(self, angle):
        if angle is not self.angle:
            pulse_width = int(servo_min + (servo_max - servo_min) * angle / 180.0)
            self.pi.set_servo_pulsewidth(self.pin, pulse_width)
        self.angle = angle
