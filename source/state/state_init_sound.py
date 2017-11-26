import pygame

from source.state.state_game import StateGame
from source.manager import Manager

class StateInitSound(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

    def first_render(self):
        self.game.clock = pygame.time.Clock()
        # titulo ventana
        pygame.display.set_caption("Medieval Brawler")

    def init_screen(self):
        self.init()
        self.render_update()