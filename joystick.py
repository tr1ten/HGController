from os import uname
from typing import Union
import uinput
import time
jmin = -127
jmax = 127
rmin = -5.0
rmax = 5.0
events = (
    uinput.ABS_X + (jmin, jmax, 0, 0),
    uinput.ABS_Y + (jmin, jmax, 0, 0),
   
	uinput.BTN_A,							#A
)

device = uinput.Device(events)


def map_value(s, a1, a2, b1, b2):
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)


def joystick_break(press):
    
    device.emit(uinput.BTN_A,press)
    
def joystick_press(val, smax=rmax, smin=rmin):
    value = int(map_value(float(val), smin, smax, jmin, jmax))
    device.emit(uinput.ABS_X, value)
    # device.emit(uinput.ABS_Y, y)
# while 1:
#     print('pressing')
#     joystick_break()
#     time.sleep(1)