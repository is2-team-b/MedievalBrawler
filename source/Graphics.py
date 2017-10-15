import pygame
import os.path
from pygame.locals import *


#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise (SystemExit, "Sorry, extended image module required")


def load_image(file, colorkey=-1):
    """loads an image, prepares it for play
    colourkey = -1 forces the left-top pixel colour to be transparent,
    use colourkey = None for non transparant surfaces """
    file = os.path.join('sprite', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise (SystemExit, 'Could not load image "%s" %s' % (file, pygame.get_error()))
    surface = surface.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0,0))
        surface.set_colorkey(colorkey, RLEACCEL)
    return surface

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def load_background(file, colorkey=-1):
    """loads an image, prepares it for play
    colourkey = -1 forces the left-top pixel colour to be transparent,
    use colourkey = None for non transparant surfaces """
    file = os.path.join('background', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise (SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error()))
    surface = surface.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0,0))
        surface.set_colorkey(colorkey, RLEACCEL)
    return surface

def load_backgrounds(*files):
    imgs = []
    for file in files:
        imgs.append(load_background(file))
    return imgs