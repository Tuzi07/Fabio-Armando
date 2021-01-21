import pyautogui
import pyttsx3
import time

engine = pyttsx3.init()

import config
import recognizer

def notify(loot):
  notification = config.get()['notification']
  engine.say(notification['message'])
  engine.runAndWait()

def click(location):
  x, y = pyautogui.position()
  pyautogui.click(*location)
  pyautogui.moveTo(x, y)

NEXT_BUTTON = config.get()['screen']['next_button']

while True:
  try:
    loot = recognizer.get_loot()
    gold, elixir, dark_elixir = loot
    print(gold, elixir, dark_elixir)
    player = config.get()['player']
    if eval(config.get()['clash']['loot'][player]):
      notify(loot)
      break
    else:
      click(NEXT_BUTTON)
  except:
    time.sleep(1)
