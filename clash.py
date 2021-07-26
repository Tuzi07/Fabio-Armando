import time

from config import Screen, Loot
import config
import utils

available_retries = config.max_retries

while True:
  i = 0
  config.setup()
  while i < config.search_limit:
    try:
      loot = Loot.recognize()
      i+=1
      print("Vila " + str(i) + "\n")
      if Loot.should_notify(loot):
        Loot.notify(loot)
        i = 0
      else:
        utils.click(Screen.next_button)
      available_retries = config.max_retries
    except Exception as error:
      if available_retries == 0:
        continue
      available_retries -= 1
      if available_retries == 0:
        available_retries = config.max_retries
        utils.click(Screen.next_button)
      time.sleep(1)
  Loot.notify_reset()
