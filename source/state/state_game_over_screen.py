import pygame

from pygame.locals import *
from source.state.state_game import StateGame
from source.manager import Manager

class StateGameOverScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Game Over screen
        self.game.gamestate = "Game Over"
        self.game.active_screen.setImage('game_over.jpg')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # update all the sprites
        self.game.all.update()

        pygame.display.update()

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def show_game_over_screen(self):
        self.waiting = True

        self.init()
        while self.waiting:
            if self.listen_events() is False: return

        for myScreen in self.game.my_screens:
            myScreen.kill()