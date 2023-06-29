import time
import pyttsx3

engine = pyttsx3.init()

import clicker
import trained_models.loot_recognizer as loot_recognizer
import trained_models.loaded_inferno_recognizer as loaded_inferno_recognizer

loot_type = "default"
message = "BIRL!"
max_retries = 3


def should_notify(loot):
    gold, elixir, dark_elixir = loot
    if loot_type == "default":
        return gold > 500000 or elixir > 500000 or dark_elixir > 4000
    if loot_type == "dark_elixir":
        return dark_elixir > 8000
    if loot_type == "inferno_unloaded":
        return (
            gold > 500000
            and elixir > 500000
            and dark_elixir > 4000
            and not loaded_inferno_recognizer.has_loaded_inferno()
        )


def notify():
    engine.say(message)
    engine.runAndWait()
    exit()


available_retries = max_retries
while True:
    loot = loot_recognizer.recognize_loot2()
    if loot:
        if should_notify(loot):
            notify()
        else:
            clicker.click_next()
        available_retries = max_retries
    else:
        if available_retries == 0:
            continue
        available_retries -= 1
        if available_retries == 0:
            available_retries = max_retries
            clicker.click_next()
        time.sleep(1)
