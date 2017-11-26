import pygame

from source.state.state_game import StateGame
from source.manager import Manager

class StateInitScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def listen_events(self):
        self.game.screenmode = input('(1-2) ')

    def process_logic(self):
        if self.game.screenmode == '1':
            bestdepth = pygame.display.mode_ok(self.game.screenrect.size, pygame.FULLSCREEN, 32)
            self.game.screen = pygame.display.set_mode(self.game.screenrect.size, pygame.FULLSCREEN, bestdepth)
        else:
            self.game.screen = pygame.display.set_mode(self.game.screenrect.size)

    def first_render(self):
        # decorate the game window
        pygame.mouse.set_visible(1)

        # create the background: tile the bgd image & draw the game maze
        # self.game.background = pygame.Surface(Game.get_instance().screenrect.size)
        self.game.background = pygame.Surface(self.game.screenrect.size)
        self.game.screen.blit(self.game.background, (0, 0))
        pygame.display.flip()

    def load_sound(self):
        self.listen_events()
        self.process_logic()
        self.render_update()