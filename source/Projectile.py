import pygame
from source import Graphics

#se anade el projectil
class Proyectile(pygame.sprite.Sprite):
    def __init__(self,pos,dirProjectile ):
        pygame.sprite.Sprite.__init__(self)
        self.image=Graphics.load_image("Proyectile2.png")
        self.rect=self.image.get_rect()
        # self.game=game
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # self.rect.center = None
        self.speed = [1 * val for val in dirProjectile]
        self.spawn_time= 1000
        self.dirProjectile = dirProjectile
        # self.gameScreen = gameScreen
        # self.gameScreen.blit(self.image, self.rect)


    def update(self):
            self.pos +=self.speed
            # self.rect.center=self.pos
            # self.rect.move_ip(self.speed)
            self.rect.center = self.pos
            # if pygame.time.get_ticks()-self.spawn_time>1000:
            #     self.kill()
