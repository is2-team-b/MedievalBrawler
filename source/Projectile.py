import pygame
from source import GameData
from source import Graphics

#se anade el projectil
class Proyectile(pygame.sprite.Sprite):
    def __init__(self,pos,dirProjectile, angleProjectile, hitboxProjectile, projectileChar, typeChar):
        pygame.sprite.Sprite.__init__(self, self.containers)
        # super(Proyectile, self).__init__()
        self.image=projectileChar
        self.rect=self.image.get_rect()
        # self.game=game
        self.pos = (pos[0],pos[1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.width = hitboxProjectile[0]
        self.rect.height = hitboxProjectile[1]
        # self.rect.center = None
        self.speed = tuple(1 * val for val in dirProjectile)
        self.spawn_time= 1000
        self.dirProjectile = dirProjectile
        self.angle = angleProjectile
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.typeChar = typeChar
        # self.image = pygame.transform.scale(self.image, (30,105))
        GameData.Game.get_instance().projectiles.add(self)
        GameData.Game.get_instance().screen.blit(self.image, self.rect)
        # self.gameScreen = gameScreen
        # self.gameScreen.blit(self.image, self.rect)

    def update(self):
            # self.pos = tuple(sum(x) for x in zip(self.pos,self.speed))
            # # self.rect.center=self.pos
            # # self.rect.move_ip(self.speed)
            # self.rect.center = self.pos
            self.rect.move_ip(self.speed)

            GameData.Game.get_instance().screen.blit(self.image, self.rect)
            # if pygame.time.get_ticks() - self.spawn_time > int(pygame.time.get_ticks() / 10) :
            for wall in GameData.Game.get_instance().battleground.walls:
                if wall.colliderect(self.rect):
                    self.kill()
