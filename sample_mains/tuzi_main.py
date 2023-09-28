import time
import pyttsx3

import clicker
import inquirer

import trained_models.loot_recognizer as loot_recognizer

# Yeti Witch
import trained_models.loaded_inferno_recognizer as loaded_inferno_recognizer

# Sgobs
# import trained_models.townhall_recognizer as townhall_recognizer
import trained_models.full_drill_recognizer as full_drill_recognizer


engine = pyttsx3.init()
running = True

loot_type = inquirer.prompt(
    [
        inquirer.List(
            "loot_type",
            message="What type of loot?",
            choices=[6, 7, 8, 9],
        )
    ]
)["loot_type"]


def should_notify(loot):
    # sgobs
    # if townhall_recognizer.is_townhall_snipable():
    #     return True

    # if fits_criteria(loot):
    #     if full_drill_recognizer.has_full_drill():
    #         return True

    # Yeti Witch
    if fits_criteria(loot):
        if not loaded_inferno_recognizer.has_loaded_inferno():
            return True

    # image_saver.print_and_save_on("database/low_loot/")
    # image_saver.print_and_save_on("database/")
    return False


def fits_criteria(loot):
    gold, elixir, dark_elixir = loot
    if loot_type == 6:
        return gold > 600000 and elixir > 600000
    if loot_type == 7:
        return gold > 700000 and elixir > 700000
    if loot_type == 8:
        return gold > 800000 and elixir > 800000
    if loot_type == 9:
        return gold > 900000 and elixir > 900000


def notify():
    engine.say("BIRL!")
    engine.runAndWait()


current_base = 1
while True:
    # time.sleep(2.4)
    time.sleep(4)
    loot = loot_recognizer.recognize_loot()
    if loot:
        print(current_base, "->", loot)
        current_base += 1
        if should_notify(loot):
            notify()
            input("Press Enter to continue...")
        else:
            clicker.click_next()
