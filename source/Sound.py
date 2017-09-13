import pygame
import os.path

class dummysound:
    def play(self): pass

def load_sound(file):
    print('Loading sounds...can I get the mixer?')
    if not pygame.mixer: return dummysound()
    print('Mixer gotten!')
    file = os.path.join('Sound', file)
    print('Sound path joined!', file)
    try:
        sound = pygame.mixer.Sound(file)
        print('Sound loaded!!!!!')
        return sound
    except pygame.error:
        print('Warning, unable to load,', file)
    return dummysound()