import pygame

from pygame.locals import *
from source.state.state_game import StateGame
from source.manager import Manager
from source.Text import draw_text

class StateMatchCompletedScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Match cleared screen
        self.game.gamestate = "Match completed"
        self.game.active_screen.setImage('game_completed.png')
        for projectile in self.game.projectiles:
            projectile.kill()
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # pintar Puntajes
        num_player_aux = 1
        y = 500
        for user in self.game.response.json()['users']:
            draw_text(self.game.screen, str(num_player_aux + user['name']), 500, y)
            draw_text(self.game.screen, user['maxKills'], 730, y)
            num_player_aux+=1
            y+=30

        # update all the sprites
        self.game.all.update()

        pygame.display.update()

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def show_match_completed_screen(self):
        self.init()

        self.waiting = True
        while self.waiting:
            if self.listen_events() is False: return

        for myScreen in self.game.my_screens:
            myScreen.kill()