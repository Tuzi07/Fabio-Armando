import pytesseract
from PIL import Image
import time
import pyscreenshot as ImageGrab

import config

custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'

def screen_grab(rect):
    x, y, width, height = rect
    im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return im

ELIXIR_COLOR = (255, 225, 253)
GOLD_COLOR = (252, 255, 201)
DARK_ELIXIR_COLOR = (243, 243, 243)

def color_in_range(color, reference):
    r, g, b = color
    rr, gr, br = reference
    color_range = 60
    return rr - color_range <= r <= rr + color_range and gr - color_range <= g <= gr + color_range and br - color_range <= b <= br + color_range

def should_paint_black(color):
    for loot_color in [ELIXIR_COLOR, GOLD_COLOR, DARK_ELIXIR_COLOR]:
        if color_in_range(color, loot_color):
            return True
    return False

def remove_noise(image):
    parent = {}
    component = {}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    width, height = image.size
    for i in range(0, width):
        for j in range(0, height):
            parent[(i, j)] = (i, j)
            component[(i, j)] = [(i, j)]

    def find(x):
        if parent[x] == x:
            return x
        parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return
        if len(component[a]) < len(component[b]):
            a, b = b, a
        parent[b] = a
        for pixel in component[b]:
            component[a].append(pixel)
        component[b] = []

    def get_component_size(pixel):
        pixel = find(pixel)
        comp = component[pixel]
        minx, maxx = width, 0
        miny, maxy = height, 0
        for pix in comp:
            minx = min(minx, pix[0])
            maxx = max(maxx, pix[0])
            miny = min(miny, pix[1])
            maxy = max(maxy, pix[1])
        return maxx - minx, maxy - miny, len(comp)

    def in_range(value, test_range):
        return test_range[0] <= value <= test_range[1]

    # create components looking at directions vector
    for i in range(width):
        for j in range(height):
            color = image.getpixel((i, j))
            if color[0] == 0:
                for k in range(len(directions)):
                    x, y = directions[k]
                    if 0 <= i+x < width and 0 <= j+y < height:
                        n_color = image.getpixel((i+x, j+y))
                        if n_color[0] == 0:
                            union((i, j), (i+x, j+y))
    # find a representative for each component
    roots = set()
    for i in range(width):
        for j in range(height):
            color = image.getpixel((i, j))
            if color[0] == 0:
                roots.add(find((i, j)))
    # paint white all too-small or too-big pixels, in any category
    noise_config = config.get()['noise']
    for root in roots:
        wd, hg, sz = get_component_size(root)
        print(wd, hg, sz)
        if not in_range(hg, noise_config['height']) or not in_range(wd, noise_config['width']) or not in_range(sz, noise_config['area']):
            for pixel in component[root]:
                image.putpixel(pixel, (255, 255, 255))
    return image

def process_image(image):
    width, height = image.size
    for i in range(width):
        for j in range(height):
            current_color = image.getpixel((i, j))
            if (should_paint_black(current_color)):
                image.putpixel((i, j), (0, 0, 0))
            else:
                image.putpixel((i, j), (255, 255, 255))
    image = remove_noise(image)

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
    text = text.splitlines()
    return (int(text[0].replace(" ", "")), int(text[1].replace(" ", "")), int(text[2].replace(" ", "")))

# returns two parameters, first is an array [gold, elixir, dark_elixir]
# and the second tells if the first one is valid or not
def get_loot(retries = 3):
    if retries == 0:
        return [], False
    screen_rect = config.get()['clash']['loot']['rect']
    image = screen_grab(screen_rect)
    process_image(image)
    image.save('test.png')
    text = pytesseract.image_to_string(image, config=custom_config).strip()
    #print(text, end='\n\n')
    if is_valid_text(text):
        return text_to_resources(text), True
    else:
        time.sleep(1)
        if len(text) > 0:
            retries -= 1 # don't use a retry if text is empty
        return get_loot(retries)


