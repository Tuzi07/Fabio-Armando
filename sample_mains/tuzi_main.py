import time
from pynput import keyboard
import pyttsx3

import clicker
import trained_models.loot_recognizer as loot_recognizer
import trained_models.full_drill_recognizer as full_drill_recognizer
import trained_models.townhall_recognizer as townhall_recognizer

# import trained_models.loaded_inferno_recognizer as loaded_inferno_recognizer

engine = pyttsx3.init()
running = True


def toggle_on_off(key):
    try:
        k = key.char
    except:
        k = key.name
    if k == "enter":
        global running
        running = not running


keyboard.Listener(on_press=toggle_on_off).start()


def should_notify(loot):
    if townhall_recognizer.is_townhall_snipable():
        return True

    if fits_criteria(loot):
        if full_drill_recognizer.has_full_drill():
            return True
        # if not loaded_inferno_recognizer.has_loaded_inferno():
        #     return True
        # image_saver.print_and_save_on("database/")

    # image_saver.print_and_save_on("database/low_loot/")
    # image_saver.print_and_save_on("database/")
    return False


def fits_criteria(loot):
    gold, elixir, dark_elixir = loot
    return gold > 500000 and elixir > 500000 and dark_elixir > 5000


def notify():
    engine.say("BIRL!")
    engine.runAndWait()


current_base = 1
while True:
    if running:
        time.sleep(3)
        loot = loot_recognizer.recognize_loot()
        if loot:
            # gold, elixir, dark_elixir = loot
            # print(current_base, "->", gold, elixir, dark_elixir)
            print(current_base, "->", loot)
            current_base += 1
            if should_notify(loot):
                running = False
                notify()
            else:
                clicker.click_next()
    else:
        time.sleep(0.5)
