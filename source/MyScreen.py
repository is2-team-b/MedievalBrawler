import pygame
import source


class MyScreen(pygame.sprite.Sprite):
    # The screen from which the player can start a new game
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = source.Graphics.load_background(image)
        self.rect = self.image.get_rect(center=source.GameData.Game.get_instance().screenrect.center)

    def setImage(self, image):
        self.image = source.Graphics.load_background(image)
        self.rect = self.image.get_rect(center=source.GameData.Game.get_instance().screenrect.center)