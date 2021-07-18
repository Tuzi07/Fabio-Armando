import pyautogui
import pyttsx3
import time

engine = pyttsx3.init()

import config
import recognizer
import eagle

def notify(loot):
  notification = config.get()['notification']
  engine.say(notification['message'])
  engine.runAndWait()

def click(location):
  x, y = pyautogui.position()
  pyautogui.click(*location)
  pyautogui.moveTo(x, y)

NEXT_BUTTON = config.get()['screen']['next_button']
MAX_RETRIES = 3

retries = MAX_RETRIES
while True:
  try:
    loot = recognizer.get_loot()
    gold, elixir, dark_elixir = loot
    unloaded = eagle.is_unloaded()
    print(gold, elixir, dark_elixir, unloaded)
    player = config.get()['player']
    if eval(config.get()['clash']['loot'][player]):
      notify(loot)
      break
    else:
      click(NEXT_BUTTON)
    retries = MAX_RETRIES
  except Exception as error:
    retries -= 1
    if retries == 0:
      retries = MAX_RETRIES
      click(NEXT_BUTTON)
    time.sleep(1)
