import pygame
import curio
import asks

from source.state.state_game import StateGame
from source.manager import Manager
from source.Flag import Flag
from source.Map import *

class StateIngameScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.playerCharacter = None
        self.playerCharacter_rect = None
        self.banderaelegida = None
        self.waiting = None
        self.condicionVictoria = None
        self.payload_to_send = None
        self.time = None

    def init(self):
        # ingame screen
        self.game.gamestate = "in game"

        scenario = self.game.response.json()['stages'][self.game.index]['scenario']
        # scenario = "river.png"

        self.game.active_screen.setImage(scenario)

        # get char elegido
        self.playerCharacter = list(filter(lambda char: char.name == self.game.player_character,
                                           self.game.playable_characters))[0]

        # get mapa elegido
        map_manager = MapManager()

        self.game.battleground = list(filter(lambda mapa: mapa.background == scenario, map_manager.maps))[0]

        self.playerCharacter_rect = Rect(self.game.battleground.respawnpoints[0],
                                         self.game.battleground.respawnpoints[1], 60, 40)

        self.playerCharacter.rect = self.playerCharacter_rect

        # banderas
        flag_rect = Rect(1120, 370, 30, 77)

        self.banderaelegida = Flag(flag_rect)


    def first_render(self):
        #set time de Juego
        self.time = pygame.time
        # pintar fondo
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        self.game.background = pygame.Surface(self.game.screenrect.size)

        for wall in self.game.battleground.walls:
            pygame.draw.rect(self.game.screen, (33, 33, 33), wall, 0)

        for pool in self.game.battleground.water:
            pygame.draw.rect(self.game.screen, (33, 33, 33), pool, 0)

        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # pintar banderas
        self.game.screen.blit(self.banderaelegida.image, self.banderaelegida.rect)

        # pintar/actualizar jugador
        self.game.screen.blit(self.playerCharacter.imageGame, self.playerCharacter.rect)

    def listen_events(self):
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):

        keystate = pygame.key.get_pressed()
        if keystate[K_UP] or keystate[K_DOWN] or keystate[K_LEFT] or keystate[K_RIGHT]\
                or (keystate[pygame.K_RIGHT] and keystate[pygame.K_UP]) or (keystate[pygame.K_LEFT] and keystate[pygame.K_UP])\
                or (keystate[pygame.K_LEFT] and keystate[pygame.K_DOWN]) or (keystate[pygame.K_RIGHT] and keystate[pygame.K_DOWN]):
            self.playerCharacter.move(keystate,self.playerCharacter)
        elif keystate[K_SPACE]:
            self.playerCharacter.shoot(self.time)

        # logica cuando agarra la bandera
        if pygame.sprite.collide_rect(self.playerCharacter, self.banderaelegida):
            self.condicionVictoria = True
            self.waiting = False

        self.game.step = self.game.step + 1
        if self.game.step > 4:
            self.game.step = 0
            self.game.animstep = self.game.animstep + 1
            if self.game.animstep > 5:
                self.game.animstep = 0

    def render_update(self):
        # update all the sprites
        self.game.all.update()

        pygame.display.flip()
        # cap the framerate
        self.game.clock.tick(int(self.game.response.json()['stages'][self.game.index]['difficulty']))
        # self.game.clock.tick(45)

    def show_stage_result_screen(self):
        self.init()

        self.waiting = True
        while self.waiting:
            self.first_render()
            if self.listen_events() is False: return
            self.process_logic()
            self.render_update()

        if self.condicionVictoria:
            self.game.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'win', 'complete'))
            self.game.index += 1
            if self.game.index > 1:
                curio.run(self.fetch('win', 'complete'))
            else:
                'Victory screen'
        else:
            self.game.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'loss', 'complete'))
            curio.run(self.fetch('loss', 'complete' if self.game.index > 1 else 'incomplete'))

    async def fetch(self, result, status):
        dict_to_send = self.get_user_payload(self.game.response.json(), result, status)
        task = await curio.spawn(asks.put('https://team-b-api.herokuapp.com/api/login/'
                                          + self.game.response.json()['loginId'] + '/', json=dict_to_send, timeout=1))
        await self.on_response_received(await task.join())

    def get_user_payload(self, json_match, result, status):
        return {'userId': json_match['userId'],
                'userName': self.game.user_name,
                'match': self.get_match_payload(json_match, result, status)}

    def get_match_payload(self, json_match, result, status):
        return {'id': json_match['matchId'],
                'result': result,
                'status': status,
                'stages': self.game.stages_to_send}

    def get_stage_payload(self, json_match, index, result, status):
        return {'id': json_match['stages'][index],
                'result': result,
                'status': status}

    async def on_response_received(self, response):
        for myScreen in self.game.my_screens:
            myScreen.kill()

        if self.condicionVictoria:
            if self.game.index > 1:
                'Match completed screen'
        else:
            'Game over screen'