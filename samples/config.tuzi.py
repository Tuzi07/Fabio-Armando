import pyttsx3
engine = pyttsx3.init()

import recognizer

message = "BIRL!"
loot_type = "default"
max_retries = 0

search_limit = 30
skipped_villages = 0
verbose = True

# runs once when program starts, can be used to change loot_type
def setup():
  import inquirer
  global loot_type
  loot_types = ['610k', '550k', '500k', '450k', '400k', '305k']
  question = [
    inquirer.List('loot_type', message="Loot Type", choices=loot_types),
  ]
  answer = inquirer.prompt(question)
  loot_type = answer['loot_type']

class Loot:
  def should_notify(loot):
    global skipped_villages
    skipped_villages+=1
    print("Vila " + str(skipped_villages) + "\n")
    if skipped_villages < search_limit:
      gold, elixir, dark_elixir = loot
      import eagle
      if loot_type == '610k':
        return gold > 610000 and elixir > 610000 and dark_elixir > 4800 and eagle.is_unloaded()
      if loot_type == '550k':
        return gold > 550000 and elixir > 550000 and dark_elixir > 4300 and eagle.is_unloaded()
      if loot_type == '500k':
        return gold > 500000 and elixir > 500000 and dark_elixir > 3900 and eagle.is_unloaded()
      if loot_type == '450k':
        return gold > 450000 and elixir > 450000 and dark_elixir > 3500 and eagle.is_unloaded()
      if loot_type == '400k':
        return gold > 400000 and elixir > 400000 and dark_elixir > 3150 and eagle.is_unloaded()
      if loot_type == '305k':
        return gold > 305000 and elixir > 305000 and dark_elixir > 2400 and eagle.is_unloaded()
    else:
      skipped_villages = 0
      engine.say("Decrease Loot Type")
      engine.runAndWait()
      setup()

  def notify(loot):
    global skipped_villages
    engine.say(message)
    engine.runAndWait()
    if input("\n : Continue\nf: Found\n\nCommand: ") == "f":
      skipped_villages = 0

  def recognize():
    loot = recognizer.loot(Screen, noise_parameters = Noise)
    gold, elixir, dark_elixir = loot
    print(gold, elixir, dark_elixir)
    return loot

class Eagle:
  scale = 0.5045454545454546
  threshold = 0.68

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
