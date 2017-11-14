# Game : this module contains all global constants & variables

import os.path

import pygame
from pygame.locals import *
import curio
import asks

from source.MyScreen import MyScreen      # MyScreen class
from source.Character import Character    # Character class
from source.Box import Box
from source import Text
from source.Flag import Flag
from source.TextInput import TextInput
from source.Map import *


class Game:

    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:

            cls.instance = Game()
            cls.state = StateInit(cls.instance)
            cls.width = 1320
            cls.height = 762
            cls.screenrect = Rect(0, 0, cls.width, cls.height)  # constant: complete window
            cls.arenarect = Rect(0, 0, cls.width, cls.height)  # constant: part of window to play in
            cls.animstep = 0  # variable: animation cycle
            cls.gamestate = "splash screen"            # variable
            cls.tile_size = 30
            cls.grid_width = cls.width / cls.tile_size
            cls.grid_height = cls.height /cls.tile_size

            cls.battleground = None
            cls.screenmode = None
            cls.active_screen = None
            cls.response = None
            cls.screen = None
            cls.background = None
            cls.music = None
            cls.clock = pygame.time.Clock()
            cls.step = None

            cls.my_screens = None
            cls.boxes = None
            cls.characters = None
            cls.player_character = None
            cls.playable_characters = None
            cls.all = None
            cls.mapElegido = []
            cls.index = None
            cls.user_name = None

        return cls.instance


class StateGame:
    def __init__(self, game):
        self.game = game

    def init_sound(self):
        pass

    def init_screen(self):
        pass

    def load_sound(self):
        pass

    def create_groups(self):
        pass

    def assign_to_groups(self):
        pass

    def show_splash_screen(self):
        pass

    def show_char_selection_screen(self):
        pass

    def show_ingame_screen(self):
        pass

    def show_stage_result_screen(self):
        pass

    def show_match_completed_screen(self):
        pass

    def show_game_over_screen(self):
        pass


class Manager:
    def init(self):
        pass

    def first_render(self):
        pass

    def listen_events(self):
        pass

    def process_logic(self):
        pass

    def render_update(self):
        pass


class StateInit(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()

    def init_sound(self):
        self.init()
        self.game.state = StateInitSound(self.game)


class StateInitSound(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

    def first_render(self):
        self.game.clock = pygame.time.Clock()
        # titulo ventana
        pygame.display.set_caption("Medieval Brawler")

    def init_screen(self):
        self.init()
        self.render_update()
        self.game.state = StateInitScreen(self.game)



class StateInitScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def listen_events(self):
        self.game.screenmode = input('(1-2) ')

    def process_logic(self):
        if self.game.screenmode == '1':
            bestdepth = pygame.display.mode_ok(Game.get_instance().screenrect.size, pygame.FULLSCREEN, 32)
            self.game.screen = pygame.display.set_mode(Game.get_instance().screenrect.size, pygame.FULLSCREEN, bestdepth)
        else:
            self.game.screen = pygame.display.set_mode(Game.get_instance().screenrect.size)

    def first_render(self):
        # decorate the game window
        pygame.mouse.set_visible(1)

        # create the background: tile the bgd image & draw the game maze
        # self.game.background = pygame.Surface(Game.get_instance().screenrect.size)
        self.game.background = pygame.Surface(self.game.screenrect.size)
        self.game.screen.blit(self.game.background, (0, 0))
        pygame.display.flip()

    def load_sound(self):
        self.listen_events()
        self.process_logic()
        self.render_update()
        self.game.state = StateLoadedSound(self.game)


class StateLoadedSound(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # load the sound effects
        if pygame.mixer:
            self.game.music = os.path.join('sound', 'lvl1_invincible.mp3')
            pygame.mixer.music.load(self.game.music)
            pygame.mixer.music.play(-1)

    def create_groups(self):
        self.init()
        self.game.state = StateCreatedGroups(self.game)


class StateCreatedGroups(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # Initialize Game Groups
        self.game.my_screens = pygame.sprite.Group()
        self.game.characters = pygame.sprite.Group()
        self.game.boxes = pygame.sprite.Group()
        self.game.all = pygame.sprite.RenderUpdates()

    def assign_to_groups(self):
        self.init()
        self.game.state = StateAssignedToGroups(self.game)


class StateAssignedToGroups(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)

    def init(self):
        # assign default groups to each sprite class
        MyScreen.containers = self.game.my_screens, self.game.all
        Character.containers = self.game.characters, self.game.all
        Box.containers = self.game.boxes, self.game.all
        self.game.step = 0  # used in calculation of animation cycles

    def show_splash_screen(self):
        self.init()
        self.game.state = StateSplashScreen(self.game)


class StateSplashScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):

        # splash screen
        Game.get_instance().gamestate = "splash screen"
        self.game.active_screen = MyScreen('splash_screen_done.png')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)
        pygame.display.update()

    def listen_events(self):
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            self.waiting = False
        self.game.step = self.game.step + 1
        if self.game.step > 4:
            self.game.step = 0
            Game.get_instance().animstep = Game.get_instance().animstep + 1
            if Game.get_instance().animstep > 5:
                Game.get_instance().animstep = 0

    def render_update(self):
        # update all the sprites
        self.game.all.update()

        # draw the scene
        dirty = self.game.all.draw(self.game.screen)
        pygame.display.update(dirty)

        # cap the framerate
        self.game.clock.tick(40)

    def show_char_selection_screen(self):
        self.init()
        self.waiting = True

        while self.waiting:
            if self.listen_events() is False: return
            self.process_logic()
            self.render_update()

        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.state = StateCharSelectionScreen(self.game)


class StateCharSelectionScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.charList = None
        self.box_rect = None
        self.box = None
        self.mousestate = None
        self.textinput = None
        self.char_name = None
        self.waiting = None
        self.collide_list = None

    def init(self):
        self.charList = [Character('Blue Crossbowman', 'blue_crossbowman.png', Rect(50, 100, 282, 440),
                              'blue_crossbowman_top_down.png'),
                    Character('Blue Mage', 'blue_mage.png', Rect(382, 100, 282, 449), 'blue_mage_top_down.png'),
                    Character('Blue Sorcerer', 'blue_sorcerer.png', Rect(714, 100, 269, 500),
                              'blue_sorcerer_top_down.png'),
                    Character('Dark Archer', 'dark_archer.png', Rect(1033, 100, 282, 374), 'dark_archer_top_down.png')]

        self.game.playable_characters = self.charList
        # Box
        self.box_rect = Rect(550, 668, 300, 90)
        self.box = Box(self.box_rect)

        # Create TextInput-object
        self.textinput = TextInput()
        self.textinput.set_text_color((255, 255, 255))

        # character selection screen
        Game.get_instance().gamestate = "character selection"
        self.game.active_screen.setImage('character_selection.png')

        self.char_name = ""
        self.game.response = None

        # Init curio
        asks.init('curio')

    def first_render(self):
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        self.collide_list = []
        for char in self.charList:
            self.collide_list.append(self.game.screen.blit(char.image, char.rect))
            if char.name == self.char_name:
                self.game.screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (134, 173, 154)),
                                      (char.rect.x + 80, char.rect.height + 130))
            else:
                self.game.screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (255, 255, 255)),
                                      (char.rect.x + 80, char.rect.height + 130))

        self.game.screen.blit(self.box.image, self.box_rect)

        textSurface = Text.loadText('Enter your nickname', 'Comic Sans MS', 20, (255, 255, 255))
        self.game.screen.blit(textSurface, (self.box_rect.x + 70, self.box_rect.y + 15))

        self.game.screen.blit(self.textinput.get_surface(), (self.box_rect.x + 70, self.box_rect.y + 50))

    def listen_events(self):
        self.mousestate = False
        # get input
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.mousestate = True
                break
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
        # Feed it with events every frame
        self.textinput.update(events)

    def process_logic(self):
        if self.mousestate:
            mouse_pos = pygame.mouse.get_pos()
            i = 0
            for char in self.charList:
                if self.collide_list[i].collidepoint(mouse_pos):
                    self.char_name = char.name
                    break
                i += 1

        keystate = pygame.key.get_pressed()
        if keystate[K_RETURN] or keystate[K_KP_ENTER]:
            if self.char_name != '' and 2 < self.textinput.get_text().__len__() < 21:
                self.waiting = False
        self.game.step = self.game.step + 1
        if self.game.step > 4:
            self.game.step = 0
            Game.get_instance().animstep = Game.get_instance().animstep + 1
            if Game.get_instance().animstep > 5:
                Game.get_instance().animstep = 0

    def render_update(self):
        # update all the sprites
        self.game.all.update()

        pygame.display.update()

        # cap the framerate
        self.game.clock.tick(40)

    def show_ingame_screen(self):
        self.init()
        self.waiting = True

        while self.waiting:
            self.first_render()
            if self.listen_events() is False: return
            self.process_logic()
            self.render_update()

        curio.run(self.fetch())

    async def fetch(self):
        self.game.player_character = self.char_name
        self.game.user_name = self.textinput.get_text()
        dict_to_send = {'userName': self.game.user_name, 'characterName': self.char_name}
        task = await curio.spawn(asks.post('https://team-b-api.herokuapp.com/api/login/',
                                           json=dict_to_send, timeout=1))
        await self.on_response_received(await task.join())

    async def on_response_received(self, response):
        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.index = 0
        self.game.response = response
        # self.game.mapElegido.append(self.game.response.json()['stages'][self.game.index]['scenario'])

        self.game.state = StateIngameScreen(self.game)


class StateIngameScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.tamano = None
        self.playerCharacter = None
        self.playerCharacter_rect = None
        self.banderaelegida = None
        self.waiting = None
        self.condicionVictoria = None
        self.payload_to_send = None
        self.stages_to_send = None

    def init(self):
        # ingame screen
        Game.get_instance().gamestate = "in game"

        scenario = self.game.response.json()['stages'][self.game.index]['scenario']

        self.game.active_screen.setImage(scenario)

        # get char elegido
        self.playerCharacter = [char for char in self.game.playable_characters if char.name == self.game.player_character][0]

        # get mapa elegido
        map_manager = MapManager()

        self.game.battleground = list(filter(lambda mapa: mapa.background == scenario, map_manager.maps))[0]

        # self.game.battleground = [mapa for mapa in map_manager.maps if mapa.background == scenario][0]

        self.playerCharacter_rect = Rect(self.game.battleground.respawnpoints[0],
                                         self.game.battleground.respawnpoints[1], 60, 40)

        self.playerCharacter.rect = self.playerCharacter_rect

        # banderas
        flag_rect = Rect(1120, 370, 30, 77)

        self.banderaelegida = Flag(flag_rect)

    def first_render(self):
        # pintar fondo
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        self.game.background = pygame.Surface(Game.get_instance().screenrect.size)

        for wall in self.game.battleground.walls:
            pygame.draw.rect(self.game.screen, (33, 33, 33), wall, 0)

        for pool in self.game.battleground.water:
            pygame.draw.rect(self.game.screen, (33, 33, 33), pool, 0)

        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # pintar banderas
        self.game.screen.blit(self.banderaelegida.image, self.banderaelegida.rect)

        # pintar jugador
        self.game.screen.blit(self.playerCharacter.imageGame, self.playerCharacter.rect)

        pygame.display.update()

    def listen_events(self):
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):
        keystate = pygame.key.get_pressed()
        if keystate[K_UP] or keystate[K_DOWN] or keystate[K_LEFT] or keystate[K_RIGHT]:
            self.playerCharacter.move(keystate)

        # logica cuando agarra la bandera
        # player_flag_collide = pygame.sprite.collide_rect_ratio(0.5)
        if pygame.sprite.collide_rect(self.playerCharacter, self.banderaelegida):
            self.condicionVictoria = True
            self.waiting = False

        self.game.step = self.game.step + 1
        if self.game.step > 4:
            self.game.step = 0
            Game.get_instance().animstep = Game.get_instance().animstep + 1
            if Game.get_instance().animstep > 5:
                Game.get_instance().animstep = 0

    def render_update(self):
        # update all the sprites
        self.game.all.update()

        pygame.display.flip()

        # cap the framerate
        self.game.clock.tick(int(self.game.response.json()['stages'][self.game.index]['difficulty']))

    def show_stage_result_screen(self):
        self.init()

        self.waiting = True
        while self.waiting:
            self.first_render()
            if self.listen_events() is False: return
            self.process_logic()
            self.render_update()

        self.stages_to_send = self.stages_to_send if self.stages_to_send is not None else []

        if self.condicionVictoria:
            self.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'win', 'complete'))
            self.game.index += 1
            if self.game.index < 2:
                self.game.state = StateVictoryScreen(self.game)
            else:
                curio.run(self.fetch('win', 'complete'))
        else:
            self.stages_to_send.append(
                self.get_stage_payload(self.game.response.json(), self.game.index, 'loss', 'complete'))
            curio.run(self.fetch('loss', 'complete' if self.game.index > 1 else 'incomplete'))



    async def fetch(self, result, status):
        dict_to_send = self.get_user_payload(self.game.response.json(), result, status)
        task = await curio.spawn(asks.put('https://team-b-api.herokuapp.com/api/login/'
                                          + self.game.response.json()['loginId'], json=dict_to_send, timeout=1))
        map(lambda x: self.on_response_received(), await task.join())

    def get_user_payload(self, json_match, result, status):
        return {'userId': json_match['userId'],
                'userName': self.game.user_name,
                'match': self.get_match_payload(json_match, result, status)}

    def get_match_payload(self, json_match, result, status):
        return {'id': json_match['matchId'],
                'result': result,
                'status': status,
                'stages': self.stages_to_send}

    def get_stage_payload(self, json_match, index, result, status):
        return {'id': json_match['stages'][index],
                'result': result,
                'status': status}

    async def on_response_received(self):
        for myScreen in self.game.my_screens:
            myScreen.kill()

        if self.condicionVictoria:
            if self.game.index > 1:
                self.game.state = StateMatchCompletedScreen(self.game)
        else:
            self.game.state = StateGameOverScreen(self.game)


class StateVictoryScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Victory screen
        Game.get_instance().gamestate = "Victory"
        self.game.active_screen.setImage(self.game.response.json()['stages'][self.game.index]['scenario'])
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # update all the sprites
        self.game.all.update()

        pygame.display.update()

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def process_logic(self):
        # Siguiente escenario
        keystate = pygame.key.get_pressed()
        if keystate[K_RETURN] or keystate[K_KP_ENTER]:
            self.waiting = False

    def show_ingame_screen(self):
        self.init()

        self.waiting = True
        while self.waiting:
            if self.listen_events() is False: return
            self.process_logic()

        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.state = StateIngameScreen(self.game)


class StateMatchCompletedScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Match cleared screen
        Game.get_instance().gamestate = "Match cleared"
        self.game.active_screen.setImage('game-completed.png')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

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


class StateGameOverScreen(StateGame, Manager):
    def __init__(self, game):
        StateGame.__init__(self, game)
        self.waiting = None

    def init(self):
        # Game Over screen
        Game.get_instance().gamestate = "Game Over"
        self.game.active_screen.setImage('game_over.jpg')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

        # update all the sprites
        self.game.all.update()

        pygame.display.update()

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    def show_game_over_screen(self):
        self.waiting = True

        self.init()
        while self.waiting:
            if self.listen_events() is False: return

        for myScreen in self.game.my_screens:
            myScreen.kill()