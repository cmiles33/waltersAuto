import os
import time
import win32api
import win32con


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Click.")

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.3)
    print('leftDown')

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')

# Basic mouse movements

def mousePos(cord):
    win32api.SetCursorPos(( cord[0], cord[1]))

def get_cords():
    x,y = win32api.GetCursorPos()
    #x = x - x_pad
    #y = y - y_pad
    return(x,y)

def clickPlace(cordx,cordy):
    mousePos((cordx,cordy))
    time.sleep(.03)
    leftDown()
    time.sleep(.03)
    leftUp()


def returnCords():
    state_left = win32api.GetKeyState(0x01)
    time.sleep(.2)
    print("before loop")
    loopBool = True
    while loopBool == True:
        a = win32api.GetKeyState(0x01)
        print("we")
        if a != state_left:
            state_left = a
            print(a)
            if a < 0:
                print('left Button Pressed')
                mouseCord = get_cords()
                loopBool = False
    return mouseCord