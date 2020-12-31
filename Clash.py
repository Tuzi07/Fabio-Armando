import sys
import pytesseract
from PIL import Image
import time
import pyscreenshot as ImageGrab
import os

COMPONENT_SIZE_RANGE = (40, 180)
HEIGHT_RANGE = (11, 15)
WIDTH_RANGE = (2, 14)

custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'

def screenGrab( rect ):
    x, y, width, height = rect
    im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return im

elixir_color = (255, 225, 253)
gold_color = (252, 255, 201)
d_elixir_color = (243, 243, 243)

def color_in_range(color, reference):
    r,g,b = color
    rr,gr,br = reference
    color_range = 60
    if rr - color_range <= r <= rr + color_range and gr - color_range <= g <= gr + color_range and br - color_range <= b <= br + color_range:
        return True
    else:
        return False

def paint_black(color):
    paint_black = False
    if color_in_range(color,elixir_color):
            paint_black = True
    if color_in_range(color,gold_color):
            paint_black = True
    if color_in_range(color,d_elixir_color):
            paint_black = True
    return paint_black

# Coordenadas para Teste
x = 285
y = 215
width = 110
height = 120

# Coordenadas do Emulador
#x = 82
#y = 193
#width = 220 - x
#height = 335 - y

screen_rect = [ x, y, width, height ]

def remove_noise(image):
    parent = {}
    component = {}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    width, height = image.size
    for i in range(0,width):
        for j in range(0,height):
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
    for root in roots:
        wd, hg, sz = get_component_size(root)
        if not in_range(hg, HEIGHT_RANGE) or not in_range(wd, WIDTH_RANGE) or not in_range(sz, COMPONENT_SIZE_RANGE):
            for pixel in component[root]:
                image.putpixel(pixel, (255,255,255))
    return image

while ( True ):
    image = screenGrab( screen_rect )        # Grab the area of the screen

    for i in range(0,width):
        for j in range(0,height):
            current_color = image.getpixel( (i,j) )
            if (paint_black(current_color)):
                image.putpixel( (i,j), (0,0,0))
            else:
                image.putpixel( (i,j), (255,255,255))
    image.save(os.path.expanduser('~/Downloads/screen_grob.png'), 'PNG')
    image = remove_noise(image)
    image.save(os.path.expanduser('~/Downloads/screen_grab.png'), 'PNG')
    text = pytesseract.image_to_string( image, config=custom_config )   # OCR the image

    text = text.strip()
    if ( len( text ) > 0 ):
        print( text, end='\n\n' )
    time.sleep(1)
