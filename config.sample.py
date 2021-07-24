import pyttsx3
engine = pyttsx3.init()

import recognizer
import eagle

message = "BIRL!"
loot_type = "default"

# runs once when program starts, can be used to change loot_type
def setup():
  # loot_type = input("Loot type = ")
  pass

class Loot:
  def should_notify(loot):
    gold, elixir, dark_elixir = loot
    if loot_type == "default":
      return gold > 500000 or elixir > 500000 or dark_elixir > 4000
    if loot_type == "dark_elixir":
      return dark_elixir > 8000

  def notify(loot):
    engine.say(message)
    engine.runAndWait()
    exit()

  def recognize():
    #loot = recognizer.loot(Screen)
    loot = recognizer.loot(Screen, noise_parameters = Noise)
    gold, elixir, dark_elixir = loot
    print(gold, elixir, dark_elixir)
    return loot

class Eagle:
  scale = 0.5045454545454546

class Screen:
  next_button = (1800, 800)
  gold        = (94, 138, 190, 30)
  elixir      = (94, 194, 190, 30)
  dark_elixir = (94, 250, 190, 30)
  loot        = (93, 135, 167, 151)

class Noise:
  width_range          = (3, 23)
  height_range         = (16, 26)
  component_size_range = (100, 380)
