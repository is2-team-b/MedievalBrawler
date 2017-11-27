import pygame
import curio
import asks

from pygame.locals import *
from source.state.state_game import StateGame
from source.manager import Manager
from source.state.state_ingame_screen import StateIngameScreen
from source.Character import Character    # Character class
from source.Box import Box
from source.TextInput import TextInput
from source import Text

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
                              'blue_crossbowman_top_down.png','ProjectileCrossbowman.png'),
                    Character('Blue Mage', 'blue_mage.png', Rect(382, 100, 282, 449), 'blue_mage_top_down.png','ProjectileMage.png'),
                    Character('Blue Sorcerer', 'blue_sorcerer.png', Rect(714, 100, 269, 500),
                              'blue_sorcerer_top_down.png','ProjectileSorcerer.png'),
                    Character('Dark Archer', 'dark_archer.png', Rect(1033, 100, 282, 374), 'dark_archer_top_down.png','ProjectileArcher.png')]

        self.game.playable_characters = self.charList
        # Box
        self.box_rect = Rect(550, 668, 300, 90)
        self.box = Box(self.box_rect)

        # Create TextInput-object
        self.textinput = TextInput()
        self.textinput.set_text_color((255, 255, 255))

        # character selection screen
        self.game.gamestate = "character selection"
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
            self.game.animstep = self.game.animstep + 1
            if self.game.animstep > 5:
                self.game.animstep = 0

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
                                           json=dict_to_send, timeout=5000))
        await self.on_response_received(await task.join())

    async def on_response_received(self, response):
        for myScreen in self.game.my_screens:
            myScreen.kill()

        self.game.index = 0
        self.game.response = response
        self.game.state = StateIngameScreen(self.game)