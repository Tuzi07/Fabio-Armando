# sample options file to establish a structure
# you should make a copy of this and rename it `options.py`

import pyautogui
import pynput
from pynput import keyboard
import pyttsx3
engine = pyttsx3.init()

class Noise:
    COMPONENT_SIZE_RANGE = (40, 180)
    HEIGHT_RANGE         = (11, 15)
    WIDTH_RANGE          = (2, 14)

class Screen:
    X      = 60
    Y      = 80
    WIDTH  = 120
    HEIGHT = 110

class Clicker:
    def notify():
        engine.say("Loot top seu vagabundo aaaa")
        engine.runAndWait()
        input("Loot Recognition Paused\nInput ENTER to continue: ")
    def click_next():
        pyautogui.click(1700,800)

class Loot:
    def is_good_loot(gold, elixir, d_elixir):
        return gold > 400000 and elixir > 400000 and d_elixir > 4000
