from tesserocr import PyTessBaseAPI, RIL, PSM, iterate_level

import parser

def parse_loot(image, threshold = 75):
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

def get_loot():
  return [parse_loot(image) for image in parser.get_images()]
