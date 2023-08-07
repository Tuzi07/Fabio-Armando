import datetime
import screen_config
from PIL import Image
import subprocess


def screen_image():
    capture_screen_cmd = ["adb", "shell", "screencap", "-p", "/sdcard/screenshot.png"]
    subprocess.run(capture_screen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pull_screen_cmd = ["adb", "pull", "/sdcard/screenshot.png"]
    subprocess.run(pull_screen_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    image = Image.open("screenshot.png")
    image = image.convert("RGB")

    return image


def rect_from_image(rect, image):
    x, y, width, height = rect
    cropped_image = image.crop((x, y, x + width, y + height))
    return cropped_image


def loot_image():
    image = screen_image()
    return rect_from_image(screen_config.loot, image)


def loot_images():
    image = screen_image()

    return [
        rect_from_image(screen_config.gold, image),
        rect_from_image(screen_config.elixir, image),
        rect_from_image(screen_config.dark_elixir, image),
    ]


def print_and_save_on(folder):
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.png")

    screenshot = screen_image()
    screenshot.save(folder + filename)
