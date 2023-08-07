import pytesseract
import platform

import screen_grabber
import imageprocessor

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        "C:/Program Files/Tesseract-OCR/tesseract.exe"
    )
from tesserocr import PyTessBaseAPI, RIL, PSM, iterate_level

tesseract_path = "./"
if platform.system() == "Windows":
    tesseract_path = "C:/Program Files/Tesseract-OCR/tessdata/"


def recognize_loot():
    image = screen_grabber.loot_image()
    # image.save("grab.png")
    processed_image = imageprocessor.processed_image(image)
    # processed_image.save("grob.png")
    # processed_image.show()
    loot = loot_from_image(processed_image)
    return loot


def loot_from_image(image):
    custom_config = r"-c tessedit_char_whitelist=0123456789 --psm 6"
    text = pytesseract.image_to_string(image, config=custom_config).strip()

    if is_valid_text(text):
        return text_to_resources(text)
    return ""


def is_valid_text(text):
    lines = text.splitlines()
    for line in lines:
        if not is_valid_number(line):
            print("Invalid text:", text)
            return False
    if len(text.splitlines()) != 3:
        print("Invalid text: not 3 numbers")
        return False
    return True


def is_valid_number(number):
    subnumbers = number.split(" ")
    for i in range(1, len(subnumbers)):
        subnumber = subnumbers[i]
        if len(subnumber) != 3:
            print("Invalid number:", number, "with subnumber", subnumber)
            screen_grabber.print_and_save_on("recognizer_fails/")
            return False
    return True


def text_to_resources(text):
    return [int(t.replace(" ", "")) for t in text.splitlines()]


def recognize_loot2():
    images = screen_grabber.loot_images()
    processed_images = [
        imageprocessor.black_text_white_background(image) for image in images
    ]
    loots = [single_line_image_to_str(image) for image in processed_images]
    for loot in loots:
        if loot == "":
            return ""
    return [int(loot) for loot in loots]


def single_line_image_to_str(image, threshold=75):
    tokens = []
    with PyTessBaseAPI(psm=PSM.SINGLE_LINE, path=tesseract_path) as api:
        api.SetImage(image)
        api.SetVariable("tessedit_char_whitelist", "0123456789")
        api.Recognize()
        ri = api.GetIterator()
        level = RIL.SYMBOL
        for r in iterate_level(ri, level):
            try:
                symbol = r.GetUTF8Text(level)
            except Exception as e:
                print("Error occurred:", str(e))
                symbol = ""
            confidence = r.Confidence(level)
            if symbol and confidence >= threshold:
                tokens.append(symbol)
    joined_tokens = "".join(tokens)
    # print("Recognized:", joined_tokens)
    # image.show()
    return joined_tokens
