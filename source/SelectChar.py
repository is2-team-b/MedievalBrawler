import pygame
from source import GameData

class SelectChar(pygame.sprite.Sprite):
    # The screen from which the player can start a new game
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(center=GameData.screenrect.center)