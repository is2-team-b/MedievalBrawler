import unittest
import pygame

from source.Character import Character
from source.MyScreen import MyScreen
from source.Projectile import Proyectile
import source


class TestCharacter(unittest.TestCase):
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

        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN

        # Posibles valores de last_angle
        # Mover izquierda: -90
        # Nover derecha: 90
        # Mover abajo: 0
        # Mover arriba: 180

    def tearDown(self):
        print('Se termina el test')

    def test_mover_izquierda(self):
        character = Character('Blue Crossbowman', 'blue_crossbowman.png', pygame.Rect(50,150, 20, 20),
                              'blue_crossbowman_top_down.png','ProjectileCrossbowman.png')
        character.move(self.left_key, character)
        self.assertEqual(character.last_angle, -90, 'Operacion mover izquierda incorrecta')

    def test_mover_bot_derecha(self):
        character = Character('Blue Crossbowman', 'blue_crossbowman.png', pygame.Rect(50,150, 20, 20),
                              'blue_crossbowman_top_down.png','ProjectileCrossbowman.png')
        character.moveBot('right', character)
        self.assertEqual(character.last_angle, 90, 'Operacion mover bot derecha incorrecta')


if __name__ == '__main__':
    unittest.main()




