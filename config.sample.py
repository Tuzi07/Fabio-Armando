import pyttsx3
engine = pyttsx3.init()

import recognizer

message = "BIRL!"
loot_type = "default"
max_retries = 3
search_limit = 30

# runs once when program starts, can be used to change loot_type
def setup():
  # import inquirer
  # global loot_type
  # loot_types = ['610k', '550k', '500k', '450k', '400k', '305k']
  # question = [
  #   inquirer.List('loot_type', message="Loot Type", choices=loot_types),
  # ]
  # answer = inquirer.prompt(question)
  # loot_type = answer['loot_type']
  pass

class Loot:
  def should_notify(loot):
    gold, elixir, dark_elixir = loot
    if loot_type == "default":
      return gold > 500000 or elixir > 500000 or dark_elixir > 4000
    if loot_type == "dark_elixir":
      return dark_elixir > 8000
    if loot_type == "eagle_unloaded":
      import eagle
      return gold > 500000 and elixir > 500000 and dark_elixir > 4000 and eagle.is_unloaded()

  def notify(loot):
    engine.say(message)
    engine.runAndWait()
    #input("\nPress ENTER to continue: ")
    exit()

  def notify_reset():
    engine.say("Decrease Loot Type")
    engine.runAndWait()

  def recognize():
    #loot = recognizer.loot(Screen)
    loot = recognizer.loot(Screen, noise_parameters = Noise)
    gold, elixir, dark_elixir = loot
    print(gold, elixir, dark_elixir)
    return loot

class Eagle:
  scale = 0.5045454545454546
  threshold = 0.6

class Screen:
  next_button = (1800, 800)
  gold        = (94, 138, 190, 30)
  elixir      = (94, 194, 190, 30)
  dark_elixir = (94, 250, 190, 30)
  loot        = (93, 135, 167, 151)
  screen      = (0, 0, 1920, 660)

class Noise:
  width_range          = (3, 23)
  height_range         = (16, 26)
  component_size_range = (100, 380)
