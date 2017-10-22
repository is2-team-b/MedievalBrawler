import pygame
from source import Graphics
from source import GameData

class Character(pygame.sprite.Sprite):
    # The character which the player will play with
    def __init__(self, name, image, rect, imageGame):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.name = name
        self.image = Graphics.load_image(image)
        self.image = pygame.transform.scale(self.image, (rect.width, rect.height))
        # Se añadio un atributo que guarda el sprite para el juego SPRINT3
        self.imageGame = Graphics.load_image(imageGame)
        self.imageGame = pygame.transform.scale(self.imageGame, (60, 80))
        self.rect = rect
        self.speed = [0, 0]

    def move(self, keyPress):
        # Buscar si se presionó flecha izquierda.
        if keyPress[pygame.K_LEFT] and self.rect.left > 0:
            self.speed = [-5, 0]
        # Si se presionó flecha derecha.
        elif keyPress[pygame.K_RIGHT] and self.rect.right < GameData.Game.get_instance().arenarect.width:
            self.speed = [5, 0]
        elif keyPress[pygame.K_DOWN] and self.rect.height < GameData.Game.get_instance().arenarect.height:
            self.speed = [0, 5]
        elif keyPress[pygame.K_UP] and self.rect.height > 0:
            self.speed = [0, -5]
        else:
            self.speed = [0, 0]
        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)