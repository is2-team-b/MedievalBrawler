from source.state.state_game import StateGame
from source.manager import Manager
from source.MyScreen import MyScreen      # MyScreen class
from source.Character import Character    # Character class
from source.Projectile import Proyectile
from source.Box import Box

class StateAssignedToGroups(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # assign default groups to each sprite class
        MyScreen.containers = self.game.my_screens, self.game.all
        Character.containers = self.game.characters, self.game.all
        Box.containers = self.game.boxes, self.game.all
        Proyectile.containers = self.game.projectiles, self.game.all
        self.game.step = 0  # used in calculation of animation cycles

    def show_splash_screen(self):
        self.init()