from tesserocr import PyTessBaseAPI, RIL, PSM, iterate_level
import pytesseract

from parser import processed_image

def single_line_image_to_int(image, threshold = 75):
  tokens = []
  with PyTessBaseAPI(psm=PSM.SINGLE_LINE) as api:
    api.SetImage(image)
    api.SetVariable("tessedit_char_whitelist", "0123456789")
    api.Recognize()
    ri = api.GetIterator()
    level = RIL.SYMBOL
    for r in iterate_level(ri, level):
      symbol = r.GetUTF8Text(level)
      confidence = r.Confidence(level)
      if symbol and confidence >= threshold:
        tokens.append(symbol)
  return int(''.join(tokens))

def loot_image_to_loot_array(image):
  def is_valid_number(text):
    sets = text.split(' ')
    for i in range(1, len(sets)):
        if len(sets[i]) != 3:
            return False
    if len(sets[0]) > 3:
        return False
    return True

  def is_valid_text(text):
      lines = text.splitlines()
      for line in lines:
          if not is_valid_number(line):
              return False
      return len(text.splitlines()) == 3

  def text_to_resources(text):
      return [int(t.replace(" ", "")) for t in text.splitlines()]

  custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
  text = pytesseract.image_to_string(image, config=custom_config).strip()
  if is_valid_text(text):
    return text_to_resources(text)
  raise Exception("invalid text")

def loot(screen, noise_parameters = None):
  if noise_parameters == None:
    loot_rects = [screen.gold, screen.elixir, screen.dark_elixir]
    loot_images = [processed_image(rect) for rect in loot_rects]
    return [single_line_image_to_int(image) for image in loot_images]
  else:
    return loot_image_to_loot_array(processed_image(screen.loot, noise_parameters))
