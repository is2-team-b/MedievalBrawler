import pygame
from source import Graphics

class Box(pygame.sprite.Sprite):
    # Just a text box
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = Graphics.load_image('box.png')
        self.rect = rect