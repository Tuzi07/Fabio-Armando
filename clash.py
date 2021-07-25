import time

from config import Screen, Loot
import config
import utils

MAX_RETRIES = 3

config.setup()

retries = MAX_RETRIES
while True:
  try:
    loot = Loot.recognize()
    if Loot.should_notify(loot):
      Loot.notify(loot)
    else:
      utils.click(Screen.next_button)
    retries = MAX_RETRIES
  except Exception as error:
    retries -= 1
    if retries == 0:
      retries = MAX_RETRIES
      utils.click(Screen.next_button)
    time.sleep(1)
