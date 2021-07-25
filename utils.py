import pyscreenshot as ImageGrab
import pyautogui

def click(location):
  x, y = pyautogui.position()
  pyautogui.click(*location)
  pyautogui.moveTo(x, y)

def screen_grab(rect):
  if rect:
    x, y, width, height = rect
    im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
  else:
    im = ImageGrab.grab()
  return im
