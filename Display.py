import curses
from Controller import XboxController
import time
import math

SOFTWARE_VERSION="v0.0.1"

class Display(object):

    def __init__(self):
        self.controller_connected = False
        self.controller = XboxController()
        self.controller.connect()
        self.screen_height = 0
        self.screen_width = 0 
        self.elevation = 0
        self.azimuth = 0
        self.fire_style_toggler = False
        curses.wrapper(self.main)

    def check_firing(self, stdscr):
        if self.controller_connected and self.controller.Get_Right_Trigger():
                if not self.fire_style_toggler: 
                    style = curses.color_pair(2)
                else: 
                    style = curses.color_pair(5)

                stdscr.addstr(self.screen_height // 2, self.screen_width // 2 - 1, "FIRE", style)
                self.fire_style_toggler = not self.fire_style_toggler
                
    def update_angles(self, x,y, amplitude):
        if self.controller_connected:
            # allow for a dead zone since joystick doesn't reset to 0 perfectly.
            if(abs(x) > 0.03 and self.azimuth + x*amplitude >= 0 and self.azimuth + x*amplitude <= 180):
                self.azimuth += x*amplitude
                self.azimuth = round(self.azimuth, 2)
            if(abs(y) > 0.03 and self.elevation + y*amplitude >= 0 and self.elevation + y*amplitude <= 180):
                self.elevation += y*amplitude
                self.elevation = round(self.elevation, 2)

    def update_angles_slow(self):
        amplitude = 2
        (x, y) = self.controller.Get_LeftXY()
        self.update_angles(x, y, amplitude)
    
    def update_angles_fast(self):
        amplitude = 7
        (x, y) = self.controller.Get_RightXY()
        self.update_angles(x, y, amplitude)

    def draw_angles_info(self, stdscr):
        stdscr.addstr(self.screen_height - 50, 2, f"Elevation: {self.elevation}", curses.A_STANDOUT)
        stdscr.addstr(self.screen_height - 52, 2, f"Azimuth: {self.azimuth}", curses.A_STANDOUT)
    
    def draw_controller_info(self, stdscr):
        stdscr.addstr(self.screen_height-2, 2, "Controller:", curses.A_STANDOUT)
        # check if the controller monitoring thread is dead
        self.controller_connected = self.controller._monitor_thread.is_alive()
        
        if self.controller_connected:
            (x, y) = self.controller.Get_RightXY()
            stdscr.addstr(self.screen_height-2, 14, f"{(round(x, 4), round(y, 4))}", curses.A_STANDOUT)
        else:
            stdscr.addstr(self.screen_height-2, 14, "DISCONNECTED", curses.color_pair(3))

    def draw_crosshair(self, stdscr):
        # Calculate the center of the screen
        center_y = self.screen_height // 2
        center_x = self.screen_width // 2
        
        # Draw horizontal line
        vertical_scale_factor = 0.4
        vertical_offset = math.floor(self.screen_height*vertical_scale_factor)
        horizontal_scale_factor = 0.40
        horizontal_offset = math.floor(self.screen_width*horizontal_scale_factor)
        for x in range(horizontal_offset, self.screen_width - horizontal_offset):
            stdscr.addch(center_y, x, '-', curses.color_pair(3))
        
        # Draw vertical line
        for y in range(vertical_offset, self.screen_height - vertical_offset):
            stdscr.addch(y, center_x, '|',curses.color_pair(3))

        # draw X
        if self.controller_connected:
            scale_factor = 0.10
            (x, y) = self.controller.Get_RightXY()
            stdscr.addch(center_y + math.floor(self.screen_height * y * scale_factor) , center_x + math.floor(self.screen_width * x * scale_factor) , 'X', curses.color_pair(5))


    def draw_angle_line(self, stdscr, y, x, length, angle):
        angle = angle % 360

        if angle in range(0, 26) or angle in range(160, 180):
            character = "_"
        elif angle in range(27, 50) or angle in range(181, 239):
            character ="\\"
        elif angle in range(51, 100) or angle in range(240, 280): 
            character = "|"
        elif angle in range(101, 160) or angle in range(281, 360): 
            character = "/"
        else:
            character="."
        angle_radians = math.radians(angle)
        adjusted_length =  math.floor(length*(0.4*((math.cos(2*angle_radians) / 2)) + 1))
    

        for i in range(adjusted_length):
            line_x = x + int(i * math.cos(angle_radians))
            line_y = y + int(i * math.sin(angle_radians))
            stdscr.addch(line_y, line_x, character)
    
    def main(self, stdscr):

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_YELLOW)


        self.screen_height, self.screen_width = stdscr.getmaxyx()
        curses.curs_set(0)
        stdscr.clear()
        stdscr.nodelay(True)

        while True:
            # Clear screen
            stdscr.clear()
            stdscr.border()
            # Get screen dimensions
            stdscr.addstr(1, 1, f"VERSION: {SOFTWARE_VERSION}", curses.color_pair(1))
            stdscr.addstr(0, self.screen_width // 2 - 7, f"SQRL CONTROL", curses.A_STANDOUT)
            self.draw_controller_info(stdscr)
            self.draw_crosshair(stdscr)
            self.check_firing(stdscr)
            self.update_angles_fast()
            self.update_angles_slow()

            self.draw_angles_info(stdscr)
            # Refresh the window to display changes
            #self.draw_angle_line(stdscr, 20, 20, 15, self.angle)

            stdscr.refresh()

            key = stdscr.getch()
            #window.getch()

            if key == ord('q') or key == ord('Q') or key == 27 or (self.controller_connected and self.controller.Get_B()):  # Check for 'q' or Escape key
               break
            time.sleep(0.1)
            # if we are disconnected, slow down loop and try to reconnect
            if not self.controller_connected:
                time.sleep(2)
                self.controller.connect()
        # Cleanup curses
        curses.endwin()

if __name__ == '__main__':
    display = Display()
    