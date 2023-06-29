import datetime
import screen_config
from PIL import ImageGrab


def loot_image():
    return image_from_rect(screen_config.loot)


def image_from_rect(rect):
    x, y, width, height = rect
    return ImageGrab.grab(bbox=(x, y, x + width, y + height), all_screens=True)


def loot_images():
    return [
        image_from_rect(screen_config.gold),
        image_from_rect(screen_config.elixir),
        image_from_rect(screen_config.dark_elixir),
    ]


def screen_image():
    return image_from_rect(screen_config.screen)


def print_and_save_on(folder):
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.png")

    screenshot = screen_image()
    screenshot.save(folder + filename)
