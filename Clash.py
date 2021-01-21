import pyautogui
import pyttsx3
import time

engine = pyttsx3.init()

import config
import parser

def notify(loot):
    notification = config.get()['notification']
    engine.say(notification['message'])
    engine.runAndWait()

def click(location):
    x, y = pyautogui.position()
    pyautogui.click(*location)
    pyautogui.moveTo(x, y)

locations = config.get()['clash']['locations']

while True:
    loot, valid = parser.get_loot()
    if valid:
        gold, elixir, d_elixir = loot
        player = config.get()['player']
        if eval(config.get()['clash']['loot']['good'][player]):
            notify(loot)
            break
        else:
            click(locations['next_button'])
    else:
        click(locations['next_button'])
