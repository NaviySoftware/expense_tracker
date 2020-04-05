import random

def color_picker():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(),r(),r())