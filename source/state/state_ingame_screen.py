import pygame
import curio
import asks
import copy

from random import randint
from source.state.state_game import StateGame
from source.manager import Manager
from source.state.state_victory_screen import StateVictoryScreen
from source.state.state_match_completed_screen import StateMatchCompletedScreen
from source.state.state_game_over_screen import StateGameOverScreen
from source.Flag import Flag
from source.Map import *
from source.DefaultBot import DefaultBot
from source.Text import draw_text

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
        self.enemiesCharacters = None
        self.botsCreados = False
        self.enemiesCreated = []

    def init(self):
        # ingame screen
        self.game.gamestate = "in game"

        scenario = self.game.response.json()['stages'][self.game.index]['scenario']
        # scenario = "ocean_wall.png"

        self.game.active_screen.setImage(scenario)

        # get char elegido
        self.playerCharacter = list(filter(lambda char: char.name == self.game.player_character,
                                           self.game.playable_characters))[0]

        # Se definen los enemigos
        self.enemiesCharacters = copy.copy(self.game.playable_characters)
        for charIte in self.enemiesCharacters:
            if charIte.name == self.playerCharacter.name:
                self.enemiesCharacters.remove(charIte)

        # get mapa elegido
        map_manager = MapManager()

        self.game.battleground = list(filter(lambda mapa: mapa.background == scenario, map_manager.maps))[0]

        self.playerCharacter_rect = Rect(self.game.battleground.respawnpoints[0],
                                         self.game.battleground.respawnpoints[1], 20, 20)

        self.playerCharacter.rect = self.playerCharacter_rect

        # banderas
        flag_rect = Rect(1120, 370, 30, 77)

        self.banderaelegida = Flag(flag_rect)


    def first_render(self):
        #set time de Juego
        self.time = pygame.time
        # pintar fondo
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # self.game.background = pygame.Surface(self.game.screenrect.size)

        for wall in self.game.battleground.walls:
            pygame.draw.rect(self.game.screen, (33, 33, 33), wall, 0)

        for pool in self.game.battleground.water:
            pygame.draw.rect(self.game.screen, (33, 33, 33), pool, 0)

        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # pintar banderas
        self.game.screen.blit(self.banderaelegida.image, self.banderaelegida.rect)

        # pintar/actualizar bots
        # cantEnemigos = 4 + 1
        cantEnemigos = self.game.response.json()['stages'][self.game.index]['numEnemies']

        if not self.botsCreados:
            for i in range(cantEnemigos):
                condicionEnemigoCreado = False
                while not condicionEnemigoCreado:
                    indiceEnemigoElegido = randint(0,2)
                    enemyChar = copy.copy(self.enemiesCharacters[indiceEnemigoElegido])
                    spawnEleg = randint(0, len(self.game.battleground.enemyrespawnpoints)-1)
                    if self.game.battleground.enemyrespawnpoints[spawnEleg][1] == 0:
                        self.game.screen.blit(enemyChar.imageGame, self.game.battleground.enemyrespawnpoints[spawnEleg][0] )
                        enemyChar.rect = self.game.battleground.enemyrespawnpoints[spawnEleg][0]
                        self.enemiesCreated.append(enemyChar)

                        # Se elimina esa opcion de respawnPoint como posibilidad
                        self.game.battleground.enemyrespawnpoints[spawnEleg][1] = 1
                        condicionEnemigoCreado = True
        else:
            for enemyCreado in self.enemiesCreated:
                self.game.screen.blit(enemyCreado.imageGame, enemyCreado.rect)

        self.botsCreados = True
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
            self.playerCharacter.shoot(self.time, "player")

        # logica cuando agarra la bandera
        if pygame.sprite.collide_rect(self.playerCharacter, self.banderaelegida):
            self.condicionVictoria = True
            self.waiting = False

        # logica de bots
        for enemyChar in self.enemiesCreated:
            DefaultBot(enemyChar,self.time)


        for projectile in self.game.projectiles:
            # logica choque proyectilEnemigo con jugador
            if projectile.typeChar == "bot":
                if pygame.sprite.collide_rect(self.playerCharacter,projectile):
                    if self.playerCharacter.hitpoints == 1:
                        self.playerCharacter.kill()
                        self.condicionVictoria = False
                        self.waiting = False
                    else:
                        self.playerCharacter.hitpoints -= 1
            # logica choque proyectilJugador con enemigo
            elif projectile.typeChar == "player":
                for enemyChar in self.enemiesCreated:
                    if pygame.sprite.collide_rect(enemyChar, projectile):
                        enemyChar.remove()
                        projectile.kill()
                        self.enemiesCreated.remove(enemyChar)
                        self.game.kills += 1

        draw_text(self.game.screen , str("Puntaje: " + str(self.game.kills)),self.game.width / 2 , 10)

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
        self.game.clock.tick(self.game.response.json()['stages'][self.game.index]['difficulty'])
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
            # # eliminar proyectiles
            # self.game.projectiles.remove()
            self.game.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'win', 'complete'))
            self.game.index += 1
            if self.game.index > 1:
                curio.run(self.fetch('win', 'complete'))
            else:
                self.game.state = StateVictoryScreen(self.game)
        else:
            self.game.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'loss', 'complete'))
            curio.run(self.fetch('loss', 'complete' if self.game.index > 1 else 'incomplete'))

    async def fetch(self, result, status):
        dict_to_send = self.get_user_payload(self.game.response.json(), result, status)
        task = await curio.spawn(asks.put('https://team-b-api.herokuapp.com/api/login/'
                                          + self.game.response.json()['loginId'] + '/', json=dict_to_send, timeout=5000))
        await self.on_response_received(await task.join())

    def get_user_payload(self, json_match, result, status):
        return {'userId': json_match['userId'],
                'userName': self.game.user_name,
                'match': self.get_match_payload(json_match, result, status)}

    def get_match_payload(self, json_match, result, status):
        return {'id': json_match['matchId'],
                'result': result,
                'status': status,
                'stages': self.game.stages_to_send,
                'kills': self.game.kills}

    def get_stage_payload(self, json_match, index, result, status):
        return {'id': json_match['stages'][index]['id'],
                'result': result,
                'status': status}

    async def on_response_received(self, response):
        for myScreen in self.game.my_screens:
            myScreen.kill()

        if self.condicionVictoria:
            if self.game.index > 1:
                self.game.response_final = response
                self.game.state = StateMatchCompletedScreen(self.game)
        else:
            self.game.state = StateGameOverScreen(self.game)