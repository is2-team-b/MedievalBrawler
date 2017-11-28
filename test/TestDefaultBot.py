import unittest
import pygame

from source.Character import Character
from source.DefaultBot import DefaultBot
from source.GameData import Game


class TestDefaultBot(unittest.TestCase):
    def setUp(self):
        print('Se inicia el test')
        pygame.init()
        pygame.mouse.set_visible(1)
        pygame.display.set_mode(Game.get_instance().screenrect.size)

    def tearDown(self):
        print('Se termina el test')

    def test_mover_bot(self):
        character_bot = Character('Blue Mage', 'blue_mage.png', pygame.Rect(100,30,60,40),
                                  'blue_mage_top_down.png','ProjectileMage.png')
        DefaultBot(character_bot, pygame.time)
        is_moving = character_bot.last_angle == 0 or character_bot.last_angle == 180 \
                    or character_bot.last_angle == 90 or character_bot.last_angle == -90
        self.assertTrue(is_moving, 'Operacion mover bot por default incorrecta')