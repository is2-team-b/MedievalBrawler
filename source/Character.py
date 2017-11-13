import pygame
from source import Graphics
from source import GameData
from source.Map import *

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
        # if not self.collide_with_obstacles():
        if keyPress[pygame.K_LEFT] and self.rect.left > 0:
            if not self.collide_with_obstacles():
                self.speed = [-5, 0]
            else:
                # for wall in GameData.Game.get_instance().battleground.walls:
                #     if wall.collidepoint(self.rect.left, self.rect.top):
                #         self.speed = [1, 0]
                #     elif wall.collidepoint(self.rect.left, self.rect.bottom):
                #         self.speed = [1, 0]
                #     elif wall.collidepoint(self.rect.left, self.rect.centery):
                #         self.speed = [1, 0]
                self.speed = [-self.speed[0],-self.speed[1]]
        elif keyPress[pygame.K_RIGHT] and self.rect.right < GameData.Game.get_instance().arenarect.width:
            if not self.collide_with_obstacles():
                self.speed = [5, 0]
            else:
                # for wall in GameData.Game.get_instance().battleground.walls:
                #     if wall.collidepoint(self.rect.right, self.rect.top):
                #         self.speed = [-1, 0]
                #     elif wall.collidepoint(self.rect.right, self.rect.bottom):
                #         self.speed = [-1, 0]
                #     elif wall.collidepoint(self.rect.right, self.rect.centery):
                #         self.speed = [-1, 0]
                # self.speed = [1, 0]
                self.speed = [-self.speed[0], -self.speed[1]]
        elif keyPress[pygame.K_DOWN] and self.rect.bottom + 10 < GameData.Game.get_instance().arenarect.height:
            if not self.collide_with_obstacles():
                self.speed = [0, 5]
            else:
                # for wall in GameData.Game.get_instance().battleground.walls:
                #     if wall.collidepoint(self.rect.left, self.rect.bottom):
                #         self.speed = [0, -1]
                #     elif wall.collidepoint(self.rect.right, self.rect.bottom):
                #         self.speed = [0, -1]
                #     elif wall.collidepoint(self.rect.centerx, self.rect.bottom):
                #         self.speed = [0, -1]
                # self.speed = [0, 1]
                self.speed = [-self.speed[0], -self.speed[1]]
        elif keyPress[pygame.K_UP] and self.rect.top - 7 > 0:
            if not self.collide_with_obstacles():
                self.speed = [0, -5]
            else:
                # for wall in GameData.Game.get_instance().battleground.walls:
                #     if wall.collidepoint(self.rect.left, self.rect.top):
                #         self.speed = [0, 1]
                #     elif wall.collidepoint(self.rect.right, self.rect.top):
                #         self.speed = [0, 1]
                #     elif wall.collidepoint(self.rect.centerx, self.rect.top):
                #         self.speed = [0, 1]
                # self.speed = [0, -1]
                self.speed = [-self.speed[0], -self.speed[1]]
        else:
            self.speed = [0, 0]

        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)

    def collide_with_obstacles(self):
        for wall in GameData.Game.get_instance().battleground.walls:
            if wall.colliderect(self.rect):
                return True
        for pool in GameData.Game.get_instance().battleground.water:
            if pool.colliderect(self.rect):
                return True
        return False

