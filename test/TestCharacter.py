import unittest
import pygame

from source.Character import Character


class TestCharacter(unittest.TestCase):
    def setUp(self):
        print('Se inicia el test')
        pygame.init()
        pygame.mouse.set_visible(1)
        
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





