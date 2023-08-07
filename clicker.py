import screen_config
import subprocess


def click_next():
    x, y = screen_config.next_button
    cmd = ["adb", "shell", f"input tap {x} {y}"]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
