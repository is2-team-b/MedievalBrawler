# Game : this module contains all global constants & variables

import os.path

import pygame
from pygame.locals import *
import requests

from source.MyScreen import MyScreen      # MyScreen class
from source.Character import Character    # Character class
from source.Box import Box
from source import Text
from source.Flag import Flag
from source.TextInput import TextInput


class Game:

    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:

            cls.instance = Game()
            cls.state = StateInit(cls.instance)
            cls.screenrect = Rect(0, 0, 1366, 768)  # constant: complete window
            cls.arenarect = Rect(0, 0, 1366, 768)  # constant: part of window to play in
            cls.animstep = 0  # variable: animation cycle
            cls.gamestate = "splash screen"            # variable

            cls.active_screen = None
            cls.response = None
            cls.screen = None
            cls.background = None
            cls.music = None
            cls.clock = None
            cls.step = None

            cls.my_screens = None
            cls.boxes = None
            cls.characters = None
            cls.player_character = None
            cls.playable_characters = None
            cls.all = None
            cls.mapElegido = []

        return cls.instance


class StateGame:
    def __init__(self, game):
        self.game = game

    def init(self):
        pass

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

    def show_game_over_screen(self):
        pass


class StateInit(StateGame):
    def init(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()

        self.game.state = StateInitSound(self.game)


class StateInitSound(StateGame):
    def init_screen(self):
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        self.game.clock = pygame.time.Clock()

        self.game.state = StateInitScreen(self.game)
        # titulo ventana
        pygame.display.set_caption("Medieval Brawler")


class StateInitScreen(StateGame):
    def load_sound(self):
        screenmode = input('(1-2) ')
        if screenmode == '1':
            bestdepth = pygame.display.mode_ok(Game.get_instance().screenrect.size, pygame.FULLSCREEN, 32)
            self.game.screen = pygame.display.set_mode(Game.get_instance().screenrect.size, pygame.FULLSCREEN, bestdepth)
        else:
            self.game.screen = pygame.display.set_mode(Game.get_instance().screenrect.size)

        # decorate the game window
        pygame.mouse.set_visible(1)

        # create the background: tile the bgd image & draw the game maze
        self.game.background = pygame.Surface(Game.get_instance().screenrect.size)
        self.game.screen.blit(self.game.background, (0, 0))
        pygame.display.flip()

        self.game.state = StateLoadedSound(self.game)


class StateLoadedSound(StateGame):
    def create_groups(self):
        # load the sound effects
        if pygame.mixer:
            self.game.music = os.path.join('sound', 'lvl1_invincible.mp3')
            pygame.mixer.music.load(self.game.music)
            pygame.mixer.music.play(-1)

        self.game.state = StateCreatedGroups(self.game)


class StateCreatedGroups(StateGame):
    def assign_to_groups(self):
        # Initialize Game Groups
        self.game.my_screens = pygame.sprite.Group()
        self.game.characters = pygame.sprite.Group()
        self.game.boxes = pygame.sprite.Group()
        self.game.all = pygame.sprite.RenderUpdates()

        self.game.state = StateAssignedToGroups(self.game)


class StateAssignedToGroups(StateGame):
    def show_splash_screen(self):
        # assign default groups to each sprite class
        MyScreen.containers = self.game.my_screens, self.game.all
        Character.containers = self.game.characters, self.game.all
        Box.containers = self.game.boxes, self.game.all
        self.game.step = 0  # used in calculation of animation cycles

        self.game.state = StateSplashScreen(self.game)


class StateSplashScreen(StateGame):
    def show_char_selection_screen(self):
        # splash screen
        Game.get_instance().gamestate = "splash screen"
        self.game.active_screen = MyScreen('splash_screen_done.png')
        self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)
        pygame.display.update()

        waiting = True
        while waiting:
            # get input
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            keystate = pygame.key.get_pressed()
            if keystate[K_SPACE]:
                waiting = False
            self.game.step = self.game.step + 1
            if self.game.step > 4:
                self.game.step = 0
                Game.get_instance().animstep = Game.get_instance().animstep + 1
                if Game.get_instance().animstep > 5:
                    Game.get_instance().animstep = 0

            # update all the sprites
            self.game.all.update()

            # draw the scene
            dirty = self.game.all.draw(self.game.screen)
            pygame.display.update(dirty)

            # cap the framerate
            self.game.clock.tick(40)

        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.state = StateCharSelectionScreen(self.game)


class StateCharSelectionScreen(StateGame):
    def show_ingame_screen(self):
        charList = [Character('Blue Crossbowman', 'blue_crossbowman.png', Rect(50, 100, 282, 440),
                              'blue_crossbowman_top_down.png'),
                    Character('Blue Mage', 'blue_mage.png', Rect(382, 100, 282, 449), 'blue_mage_top_down.png'),
                    Character('Blue Sorcerer', 'blue_sorcerer.png', Rect(714, 100, 269, 500),
                              'blue_sorcerer_top_down.png'),
                    Character('Dark Archer', 'dark_archer.png', Rect(1033, 100, 282, 374), 'dark_archer_top_down.png')]

        self.game.playable_characters = charList
        # Box
        box_rect = Rect(550, 668, 300, 90)
        box = Box(box_rect)

        # Create TextInput-object
        textinput = TextInput()
        textinput.set_text_color((255, 255, 255))

        # character selection screen
        Game.get_instance().gamestate = "character selection"
        self.game.active_screen.setImage('character_selection.png')

        char_name = ""
        waiting = True
        self.game.response = None
        while waiting:

            self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

            collide_list = []
            for char in charList:
                collide_list.append(self.game.screen.blit(char.image, char.rect))
                if char.name == char_name:
                    self.game.screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (134, 173, 154)),
                                     (char.rect.x + 80, char.rect.height + 130))
                else:
                    self.game.screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (255, 255, 255)),
                                     (char.rect.x + 80, char.rect.height + 130))

            self.game.screen.blit(box.image, box_rect)

            textSurface = Text.loadText('Enter your nickname', 'Comic Sans MS', 20, (255, 255, 255))
            self.game.screen.blit(textSurface, (box_rect.x + 70, box_rect.y + 15))

            self.game.screen.blit(textinput.get_surface(), (box_rect.x + 70, box_rect.y + 50))

            mousestate = False
            # get input
            events = pygame.event.get()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    mousestate = True
                    break
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    break

            # Feed it with events every frame
            textinput.update(events)

            if mousestate:
                mouse_pos = pygame.mouse.get_pos()
                i = 0
                for char in charList:
                    if collide_list[i].collidepoint(mouse_pos):
                        char_name = char.name
                        break
                    i += 1

            keystate = pygame.key.get_pressed()
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                if char_name != '' and 2 < textinput.get_text().__len__() < 21:
                    # payload = {'name': textinput.get_text(), }
                    # requests.post('https://team-b-api.herokuapp.com/api/user/', json=payload)
                    payload = {'userName': textinput.get_text(), 'characterName': char_name}
                    self.game.response = requests.post('https://team-b-api.herokuapp.com/api/login/', json=payload)
                    self.game.player_character = char_name
                    waiting = False
            self.game.step = self.game.step + 1
            if self.game.step > 4:
                self.game.step = 0
                Game.get_instance().animstep = Game.get_instance().animstep + 1
                if Game.get_instance().animstep > 5:
                    Game.get_instance().animstep = 0

            # update all the sprites
            self.game.all.update()

            pygame.display.update()

            # cap the framerate
            self.game.clock.tick(40)

        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.mapElegido.push(self.game.response.json()['scenario'])

        self.game.state = StateIngameScreen(self.game)


class StateIngameScreen(StateGame):
    def show_game_result_screen(self):
        # ingame screen
        Game.get_instance().gamestate = "in game"

        # mapElegido = "ocean_wall.png"
        print(self.game.mapElegido)

        self.game.active_screen.setImage(self.game.mapElegido)

        # get char elegido
        playerCharacter = [char for char in self.game.playable_characters if char.name == self.game.player_character][0]

        # mapElegido.posicionJugador busca setear la posicion inicial del jugador geteando un atributo establecido en el mapa a jugar
        # Sin embargo response.json()['scenario'] solo trae el nombre en string, evaluar si se puede traer el objeto completo del mapa
        # screen.blit(playerCharacter.imageGame, mapElegido.posicionJugador )
        playerCharacter_rect = Rect(50, 150, 55, 160)

        playerCharacter.rect = playerCharacter_rect

        # banderas
        flag_rect = Rect(600, 480, 630, 500)

        banderaelegida = Flag(flag_rect)

        waiting = True
        while waiting:

            # pintar fondo
            self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)

            # pintar banderas
            self.game.screen.blit(banderaelegida.image, banderaelegida.rect)

            # pintar jugador
            self.game.screen.blit(playerCharacter.imageGame, playerCharacter.rect)

            # get input
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return

            keystate = pygame.key.get_pressed()
            if keystate[K_UP] or keystate[K_DOWN] or keystate[K_LEFT] or keystate[K_RIGHT]:
                playerCharacter.move(keystate)

            # logica cuando agarra la bandera
            # player_flag_collide = pygame.sprite.collide_rect_ratio(0.5)
            if pygame.sprite.collide_rect(playerCharacter, banderaelegida):
                condicionVictoria = True
                waiting = False

            self.game.step = self.game.step + 1
            if self.game.step > 4:
                self.game.step = 0
                Game.get_instance().animstep = Game.get_instance().animstep + 1
                if Game.get_instance().animstep > 5:
                    Game.get_instance().animstep = 0

            # update all the sprites
            self.game.all.update()

            pygame.display.flip()

            # cap the framerate
            self.game.clock.tick(int(self.game.response.json()['difficulty']))

        for myScreen in self.game.my_screens:
            myScreen.kill()

        if condicionVictoria:
            self.game.active_screen.setImage('victory_screen.png')

            self.game.screen.blit(self.game.active_screen.image, self.game.active_screen.rect)
            self.game.all.update()

            pygame.display.update()

            self.game.state = StateVictoryScreen(self.game)
        else:
            self.game.state = StateGameOverScreen(self.game)



class StateVictoryScreen(StateGame):
    def show_splash_screen(self):
        waiting = True

        while waiting:

            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        #Siguiente escenario
            keystate = pygame.key.get_pressed()
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                if self.game.mapElegido == "ocean_wall.png":
                    self.game.mapElegido = "river.png"
                    waiting=False
                else:
                    self.game.mapElegido = "ocean_wall.png"
                    waiting = False
        for myScreen in self.game.my_screens:
            myScreen.kill()
        self.game.state = StateIngameScreen(self.game)



class StateGameOverScreen(StateGame):
    pass
