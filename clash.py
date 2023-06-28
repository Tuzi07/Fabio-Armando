import time

from config import Screen, Loot
import config
import utils

config.setup()

available_retries = config.max_retries
while True:
    try:
        loot = Loot.recognize()
        if Loot.should_notify(loot):
            Loot.notify(loot)
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
