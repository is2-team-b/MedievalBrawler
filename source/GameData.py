# Game : this module contains all global constants & variables

import pygame

from pygame.locals import *
from source.state.state_init import StateInit


class Game:

    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:

            cls.instance = Game()
            cls.state = StateInit(cls.instance)
            cls.width = 1320
            cls.height = 762
            cls.screenrect = Rect(0, 0, cls.width, cls.height)  # constant: complete window
            cls.arenarect = Rect(0, 0, cls.width, cls.height)  # constant: part of window to play in
            cls.animstep = 0  # variable: animation cycle
            cls.gamestate = "splash screen"            # variable
            cls.tile_size = 30
            cls.grid_width = cls.width / cls.tile_size
            cls.grid_height = cls.height /cls.tile_size

            cls.battleground = None
            cls.screenmode = None
            cls.active_screen = None
            cls.response = None
            cls.response_final = None
            cls.screen = None
            cls.background = None
            cls.music = None
            cls.clock = pygame.time.Clock()
            cls.step = None
            cls.kills = 0

            cls.my_screens = None
            cls.boxes = None
            cls.characters = None
            cls.player_character = None
            cls.playable_characters = None
            cls.all = None
            cls.index = None
            cls.user_name = None
            cls.stages_to_send = []

        return cls.instance