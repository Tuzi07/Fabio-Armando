from PIL import Image
import pyscreenshot as ImageGrab

import config

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
    if color_in_range(color, loot_color): return True
  return False

def remove_noise(image, noise_parameters):
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

  def get_component_sizes(pixel):
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

  # paint white all components that are too small or too big
  if noise_parameters == None:
    HEIGHT_THRESHOLD = 0.5
    for root in roots:
      _, component_height, _ = get_component_sizes(root)
      relative_height = component_height / height
      if relative_height < HEIGHT_THRESHOLD:
        for pixel in component[root]:
          image.putpixel(pixel, (255, 255, 255))
  else:
    for root in roots:
      wd, hg, sz = get_component_sizes(root)
      if not in_range(hg, noise_parameters.height_range) or not in_range(wd, noise_parameters.width_range) or not in_range(sz, noise_parameters.component_size_range):
        for pixel in component[root]:
          image.putpixel(pixel, (255, 255, 255))

  return image

def processed_image(rect, noise_parameters = None):
  image = screen_grab(rect)
  width, height = image.size
  for i in range(width):
    for j in range(height):
      current_color = image.getpixel((i, j))
      if (should_paint_black(current_color)):
        image.putpixel((i, j), (0, 0, 0))
      else:
        image.putpixel((i, j), (255, 255, 255))
  image = remove_noise(image, noise_parameters)
  return image
