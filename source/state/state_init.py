import pygame

from source.manager import Manager
from source.state.state_game import StateGame

class StateInit(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()

    def init_sound(self):
        self.init()