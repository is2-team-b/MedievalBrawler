import pygame
from source import Graphics


class Character(pygame.sprite.Sprite):
    # The character which the player will play with
    def __init__(self, name, image, rect):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.name = name
        self.image = Graphics.load_image(image)
        self.image = pygame.transform.scale(self.image, (rect.width, rect.height))
        self.rect = rect
