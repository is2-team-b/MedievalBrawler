import pygame

from pygame.locals import *
from source.state.state_game import StateGame
from source.manager import Manager
import source

class StateVictoryScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Victory screen
        self.game.gamestate = "Victory"
        self.game.active_screen.setImage('victory_screen.png')
        for projectile in self.game.projectiles:
            projectile.kill()
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # update all the sprites
        self.game.all.update()

        pygame.display.update()

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):
        # Siguiente escenario
        keystate = pygame.key.get_pressed()
        if keystate[K_RETURN] or keystate[K_KP_ENTER]:
            self.waiting = False

    def show_ingame_screen(self):
        self.init()

        self.waiting = True
        while self.waiting:
            if self.listen_events() is False: return
            self.process_logic()

        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.state = source.StateIngameScreen(self.game)