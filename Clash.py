import sys
import pytesseract
from PIL import Image
import time
from Xlib import display, X   

custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'

def screenGrab( rect ):
    x, y, width, height = rect

    dsp  = display.Display()
    root = dsp.screen().root
    raw_image = root.get_image( x, y, width, height, X.ZPixmap, 0xffffffff )
    image = Image.frombuffer( "RGB", ( width, height ), raw_image.data, "raw", "BGRX", 0, 1 )
    #image.save( '/home/tuzi/Downloads/screen_grab.png', 'PNG' )
    return image

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
x = 123
y = 222
width = 150
height = 144

# Coordenadas do Emulador
#x = 93
#y = 166
#width = 147
#height = 151

screen_rect = [ x, y, width, height ]


while ( True ):
    image = screenGrab( screen_rect )        # Grab the area of the screen
    

    for i in range(0,width):
        for j in range(0,height):
            current_color = image.getpixel( (i,j) )
            if (paint_black(current_color)):
                image.putpixel( (i,j), (0,0,0))
            else:
                image.putpixel( (i,j), (255,255,255))

    image.save( '/home/tuzi/Downloads/screen_grab.png', 'PNG' )
    text = pytesseract.image_to_string( image, config=custom_config )   # OCR the image

    text = text.strip()
    if ( len( text ) > 0 ):
        print( text + "\n\n\n\n\n\n\n\n\n\n" )
    time.sleep(1)
