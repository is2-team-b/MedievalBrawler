import unittest
import pygame

from source.Character import Character
from source.GameData import Game
from source.MyScreen import MyScreen


class TestCharacter(unittest.TestCase):
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




