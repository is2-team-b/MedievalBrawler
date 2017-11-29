import unittest
import pygame

from source.Character import Character
from source.DefaultBot import DefaultBot
from source.GameData import Game
from source.MyScreen import MyScreen


class TestDefaultBot(unittest.TestCase):
    def setUp(self):
        print('Se inicia el test')

        pygame.init()
        pygame.font.init()
        Game.get_instance().screen = pygame.display.set_mode(Game.get_instance().screenrect.size)

        pygame.mouse.set_visible(1)
        Game.get_instance().background = pygame.Surface(Game.get_instance().screenrect.size)
        pygame.Surface(Game.get_instance().screenrect.size)
        Game.get_instance().screen.blit(Game.get_instance().background, (0, 0))
        pygame.display.flip()

        Game.get_instance().my_screens = pygame.sprite.Group()
        Game.get_instance().characters = pygame.sprite.Group()
        Game.get_instance().all = pygame.sprite.RenderUpdates()

        MyScreen.containers = Game.get_instance().my_screens, Game.get_instance().all
        Character.containers = Game.get_instance().characters, Game.get_instance().all

        Game.get_instance().active_screen = MyScreen('splash_screen_done.png')
        Game.get_instance().screen.blit(Game.get_instance().active_screen.image, Game.get_instance().active_screen.rect)
        pygame.display.update()

    def tearDown(self):
        print('Se termina el test')

    def test_mover_bot(self):
        character_bot = Character('Blue Mage', 'blue_mage.png', pygame.Rect(100,30,60,40),
                                  'blue_mage_top_down.png','ProjectileMage.png')
        DefaultBot(character_bot, pygame.time)
        is_moving = character_bot.last_angle == 0 or character_bot.last_angle == 180 \
                    or character_bot.last_angle == 90 or character_bot.last_angle == -90
        self.assertTrue(is_moving, 'Operacion mover bot por default incorrecta')


if __name__ == '__main__':
    unittest.main()