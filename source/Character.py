import pygame
from source import Graphics
from source import GameData
from source.Projectile import Proyectile
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
        self.last_shot = 0
        self.last_dir = [1,0]

    def move(self, keyPress, char):
        # if not self.collide_with_obstacles():
        if keyPress[pygame.K_LEFT] and self.rect.left > 0:
            if not self.collide_with_obstacles():
                self.speed = [-5, 0]
                char.last_dir = self.speed
            else:
                self.speed = [-self.speed[0],-self.speed[1]]
        elif keyPress[pygame.K_RIGHT] and self.rect.right < GameData.Game.get_instance().arenarect.width:
            if not self.collide_with_obstacles():
                self.speed = [5, 0]
                char.last_dir = self.speed
            else:
                self.speed = [-self.speed[0], -self.speed[1]]
        elif keyPress[pygame.K_DOWN] and self.rect.bottom + 10 < GameData.Game.get_instance().arenarect.height:
            if not self.collide_with_obstacles():
                self.speed = [0, 5]
                char.last_dir = self.speed
            else:
                self.speed = [-self.speed[0], -self.speed[1]]
        elif keyPress[pygame.K_UP] and self.rect.top - 7 > 0:
            if not self.collide_with_obstacles():
                self.speed = [0, -5]
                char.last_dir = self.speed
            else:
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

    def shoot(self, time):
        now = time.get_ticks()
        if now - self.last_shot > 170:
            self.last_shot = now
            dirProjectile = self.last_dir
            pos = self.rect.center
            charProyectil = Proyectile( pos, dirProjectile)
            return charProyectil







