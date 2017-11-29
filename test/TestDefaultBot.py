import unittest
import pygame

from source.Character import Character
from source.DefaultBot import DefaultBot
from source.Projectile import Proyectile
from source.MyScreen import MyScreen
import source


class TestDefaultBot(unittest.TestCase):
    def setUp(self):
        print('Se inicia el test')

        pygame.init()
        pygame.font.init()
        source.GameData.Game.get_instance().screen = pygame.display.set_mode(source.GameData.Game.get_instance().screenrect.size)

        pygame.mouse.set_visible(1)
        source.GameData.Game.get_instance().background = pygame.Surface(source.GameData.Game.get_instance().screenrect.size)
        pygame.Surface(source.GameData.Game.get_instance().screenrect.size)
        source.GameData.Game.get_instance().screen.blit(source.GameData.Game.get_instance().background, (0, 0))
        pygame.display.flip()

        source.GameData.Game.get_instance().my_screens = pygame.sprite.Group()
        source.GameData.Game.get_instance().characters = pygame.sprite.Group()
        source.GameData.Game.get_instance().projectiles = pygame.sprite.Group()
        source.GameData.Game.get_instance().all = pygame.sprite.RenderUpdates()

        MyScreen.containers = source.GameData.Game.get_instance().my_screens, source.GameData.Game.get_instance().all
        Character.containers = source.GameData.Game.get_instance().characters, source.GameData.Game.get_instance().all
        Proyectile.containers = source.GameData.Game.get_instance().projectiles, source.GameData.Game.get_instance().all

        source.GameData.Game.get_instance().active_screen = MyScreen('splash_screen_done.png')
        source.GameData.Game.get_instance().screen.blit(source.GameData.Game.get_instance().active_screen.image,
                                                        source.GameData.Game.get_instance().active_screen.rect)
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