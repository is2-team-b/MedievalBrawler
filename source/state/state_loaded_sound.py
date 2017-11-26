import os.path
import pygame

from source.state.state_game import StateGame
from source.manager import Manager

class StateLoadedSound(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # load the sound effects
        if pygame.mixer:
            self.game.music = os.path.join('sound', 'lvl1_invincible.mp3')
            pygame.mixer.music.load(self.game.music)
            pygame.mixer.music.play(-1)

    def create_groups(self):
        self.init()