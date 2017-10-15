import pygame
from source import GameData


#####################################################################
class GameOver(pygame.sprite.Sprite):
    """Game Over screen"""
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=GameData.screenrect.center)