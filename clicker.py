import pyautogui
import screen_config


def click_next():
    x, y = pyautogui.position()
    pyautogui.click(screen_config.next_button)
    pyautogui.moveTo(x, y)
