import sys
import pytesseract
from PIL import Image
import time
import pyscreenshot as ImageGrab

custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'

def screenGrab(rect):
    x, y, width, height = rect
    im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return im

elixir_color = (255, 225, 253)
gold_color = (252, 255, 201)
d_elixir_color = (243, 243, 243)

def color_in_range(color, reference):
    r, g, b = color
    rr, gr, br = reference
    color_range = 60
    return rr - color_range <= r <= rr + color_range and gr - color_range <= g <= gr + color_range and br - color_range <= b <= br + color_range


def paint_black(color):
    return color_in_range(color, elixir_color) or color_in_range(color, gold_color) or color_in_range(color, d_elixir_color)

# Pedro: Coordenadas do Emulador
x = 285
y = 215
width = 110
height = 120

# Pedro: Coordenadas para Teste
# x = 82
# y = 193
# width = 220 - x
# height = 335 - y

# Tuzi: Coordenadas para Teste
# x = 123
# y = 222
# width = 150
# height = 144

# Tuzi: Coordenadas do Emulador
# x = 93
# y = 166
# width = 147
# height = 151

screen_rect = [x, y, width, height]

p = {}
w = {}

def reset():
    global p, w
    p = {}
    w = {}
    for i in range(0, width):
        for j in range(0, height):
            p[(i, j)] = (i, j)
            w[(i, j)] = 1

adj = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def find(x):
    global p
    if p[x] == x:
        return x
    p[x] = find(p[x])
    return p[x]

def union(a, b):
    global p, w
    a = find(a)
    b = find(b)
    if a == b:
        return
    if w[a] < w[b]:
        a, b = b, a
    w[a] += w[b]
    p[b] = a

while True:
    image = screenGrab(screen_rect)

    reset()
    for i in range(0, width):
        for j in range(0, height):
            current_color = image.getpixel((i, j))
            if paint_black(current_color):
                image.putpixel((i, j), (0, 0, 0))
            else:
                image.putpixel((i, j), (255, 255, 255))
    for i in range(0, width):
        for j in range(0, height):
            color = image.getpixel((i, j))
            if color[0] == 0:
                for k in range(len(adj)):
                    x, y = adj[k]
                    if 0 <= i + x < width and 0 <= j + y < height:
                        n_color = image.getpixel((i + x, j + y))
                        if n_color[0] == 0:
                            union((i, j), (i + x, j + y))

    # image.save( '/home/pedroteosousa/Downloads/screen_grob.png', 'PNG' )
    # image.save( '/home/tuzi/Downloads/new/screen_grob.png', 'PNG' )

    t = {}
    for i in range(0, width):
        for j in range(0, height):
            color = image.getpixel((i, j))

            if color[0] == 0 and (w[find((i, j))] < 60 or w[find((i, j))] > 220): # PEDRO
            # if color[0] == 0 and (w[find((i, j))] < 60 or w[find((i, j))] > 331):  # TUZI
                image.putpixel((i, j), (255, 255, 255))
                t[find((i, j))] = w[find((i, j))]
    for a in t:
        pass
        # print (t[a])

    text = pytesseract.image_to_string(image, config=custom_config)

    # image.save( '/home/pedroteosousa/Downloads/screen_grab.png', 'PNG' )
    # image.save( '/home/tuzi/Downloads/new/screen_grab.png', 'PNG' )

    text = text.strip()
    if len(text) > 0:
        print(text, end='\n\n')
    time.sleep(1)
