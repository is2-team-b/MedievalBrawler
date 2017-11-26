import pygame

from pygame.locals import *
from source.state.state_game import StateGame
from source.manager import Manager
from source.MyScreen import MyScreen      # MyScreen class

class StateSplashScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):

        # splash screen
        self.game.gamestate = "splash screen"
        self.game.active_screen = MyScreen('splash_screen_done.png')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)
        pygame.display.update()

    def listen_events(self):
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            self.waiting = False
        self.game.step = self.game.step + 1
        if self.game.step > 4:
            self.game.step = 0
            self.game.animstep = self.game.animstep + 1
            if self.game.animstep > 5:
                self.game.animstep = 0

    def render_update(self):
        # update all the sprites
        self.game.all.update()

        # draw the scene
        dirty = self.game.all.draw(self.game.screen)
        pygame.display.update(dirty)

        # cap the framerate
        self.game.clock.tick(40)

    def show_char_selection_screen(self):
        self.init()
        self.waiting = True

        while self.waiting:
            if self.listen_events() is False: return
            self.process_logic()
            self.render_update()

        for myScreen in self.game.my_screens:
            myScreen.kill()