import pygame
from source import GameData
from source import Graphics

class MyScreen(pygame.sprite.Sprite):
    # The screen from which the player can start a new game
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = Graphics.load_background(image)
        self.rect = self.image.get_rect(center=GameData.screenrect.center)

    def setImage(self, image):
        self.image = Graphics.load_background(image)
        self.rect = self.image.get_rect(center=GameData.screenrect.center)