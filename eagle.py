import numpy as np
import cv2
import imutils
import os

from PIL import Image
import pyscreenshot as ImageGrab

import config

def is_unloaded():
    def search(image_path, structure_path, scale):
        template = cv2.imread(structure_path)
        image_o = cv2.imread(image_path)

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)

        resized = imutils.resize(template, width = int(template.shape[1] * scale))

        w, h = resized.shape[::-1]
        a, b = image.shape[::-1]
        x = 0
        if w > a or h > b:
            return 0, None, None
        try:
            res = cv2.matchTemplate(image,resized,cv2.TM_CCOEFF_NORMED, x, resized)
        except Exception as err:
            print(err)
            return

        return res, (w, h)

    ASSETS_LOCATION = "assets"

    def find_best_fit(image_path, structure_name, scale):
        base_path = os.path.join(ASSETS_LOCATION, structure_name)
        best_fit = 0
        for path in os.listdir(base_path):
            structure_path = os.path.join(base_path, path)
            res, size = search(image_path, structure_path, scale)
            best_fit = max(best_fit, np.max(res))
        return best_fit

    image_path = "base.png"
    ImageGrab.grab().save(image_path)

    scale = config.get()['scale']
    THRESHOLD = 0.6
    best_fit_loaded = find_best_fit(image_path, 'eagle', scale)
    best_fit_unloaded = find_best_fit(image_path, 'eagle_unloaded', scale)

    return best_fit_unloaded > THRESHOLD and best_fit_unloaded > best_fit_loaded

if __name__ == '__main__':
    print('unloaded =', is_unloaded())
