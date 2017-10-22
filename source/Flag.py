import pygame
from source import Graphics

class Flag(pygame.sprite.Sprite):
    # Just a text box
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = Graphics.load_image('banderaAzul.png')
        # self.image = pygame.transform.scale(self.image, (rect.width, rect.height))
        self.rect = rect