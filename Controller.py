from inputs import get_gamepad
import evdev
import math
import threading
import time;

# https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    
    def __init__(self):
        self.gamepad = None
        self.LeftJoystickY = 1
        self.LeftJoystickX = 1
        self.RightJoystickY = 1
        self.RightJoystickX = 1
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

    def connect(self):
        self.gamepad = evdev.InputDevice(evdev.list_devices()[0])
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def Get_B(self):
        return self.B

    def Get_Right_Trigger(self):
        return self.RightTrigger/4

    def Get_LeftXY(self):
	# map 0-2 to -1 1
        return (self.LeftJoystickX-1, -1*(self.LeftJoystickY-1))

    def Get_RightXY(self):
        return (self.RightJoystickX-1, -1*(self.RightJoystickY-1))

    def read(self): # return the buttons/triggers that you care about in this methode
        x = self.LeftJoystickX
        y = self.LeftJoystickY

        a = self.A
        b = self.X # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]

    def is_available(self):
        # this is a hack, but if only have 1 device "eg. event0, it's not connected."
        return len(evdev.list_devices()) > 1

    def _monitor_controller(self):
        for event in self.gamepad.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                absevent = evdev.categorize(event)
                val = (absevent.event.value / XboxController.MAX_JOY_VAL)
                #print(absevent.event.code)
                if absevent.event.code == 0:
                    self.LeftJoystickX = val
                elif absevent.event.code == 1:
                    self.LeftJoystickY = val
                elif absevent.event.code == 2:
                    self.RightJoystickX = val
                elif absevent.event.code == 5:    
                    self.RightJoystickY = val
                elif absevent.event.code == 9:    
                    self.RightTrigger = absevent.event.value / XboxController.MAX_TRIG_VAL

            elif event.type == evdev.ecodes.EV_KEY:
                keyevent = evdev.categorize(event)
                if keyevent.keystate == 1:  # Key press
                    #print(f"Button {keyevent.keycode[0]} pressed")
                    if keyevent.keycode[0] == "BTN_B":
                        self.B = 1
                    
                elif keyevent.keystate == 0:  # Key release
                    #print(f"Button {keyevent.keycode[0]} released")
                    if keyevent.keycode[0] == "BTN_B":
                        self.B = 0

if __name__ == '__main__':
    joy = XboxController()
    joy.connect()
    while True:
        print(joy.Get_LeftXY(), joy.Get_RightXY(), joy.Get_B(), joy.Get_Right_Trigger())
        time.sleep(1)
