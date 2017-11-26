import pygame

from source.state.state_game import StateGame
from source.manager import Manager

class StateCreatedGroups(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # Initialize Game Groups
        self.game.my_screens = pygame.sprite.Group()
        self.game.characters = pygame.sprite.Group()
        self.game.boxes = pygame.sprite.Group()
        self.game.projectiles = pygame.sprite.Group()
        self.game.all = pygame.sprite.RenderUpdates()

    def assign_to_groups(self):
        self.init()