import os.path

import pygame
from pygame.locals import *
import requests

from source import GameData, Graphics   # contains all global variables
from source import SelectChar           # Character selection screen class
from source import MyScreen             # MyScreen class
from source import GameOver             # Game Over screen class
from source import Character            # Character class
from source import Box
from source import Text
from source import TextInput

# Classes
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# Functions
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

def main():
    # Initialize pygame
    pygame.init()
    pygame.font.init()

    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    clock = pygame.time.Clock()

    screenmode = input('(1-2) ')
    if screenmode == '1':
        bestdepth = pygame.display.mode_ok(GameData.screenrect.size, pygame.FULLSCREEN, 32)
        screen = pygame.display.set_mode(GameData.screenrect.size, pygame.FULLSCREEN, bestdepth)
    else:
        screen = pygame.display.set_mode(GameData.screenrect.size)

    # Load images, assign to sprite classes (Linux/Unix filenames are case sensitive)

    # SplashScreen.image = Graphics.load_background('splash_screen_done.png')
    # SelectChar.image = Graphics.load_background('character_selection.png')
    # GameOver.images = [Graphics.load_background('game_over.jpg')]
    # Character.images = Graphics.load_images('blue_crossbowman.png', 'blue_mage.png', 'blue_sorcerer.png', 'dark_archer.png')

    # decorate the game window
    pygame.mouse.set_visible(1)

    # create the background: tile the bgd image & draw the game maze
    background = pygame.Surface(GameData.screenrect.size)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #load the sound effects
    if pygame.mixer:
        music = os.path.join('sound', 'intro_wolf_king.mp3')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    # Initialize Game Groups
    myScreens = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    MyScreen.containers = myScreens, all
    Character.containers = characters, all
    Box.containers = boxes, all

    # Initialise sprites
    # splashScreenSprite = pygame.sprite.RenderPlain(splashScreen)
    # selectCharScreenSprite = pygame.sprite.RenderPlain(selectCharScreen)
    # gameOverScreenSprite = pygame.sprite.RenderPlain(gameOverScreen)
    # boxSprite = pygame.sprite.RenderPlain(box)
    step = 0  # used in calculation of animation cycles

    # main loop
    while True:
        # splash screen
        GameData.gamestate = "splash screen"
        activeScreen = MyScreen('splash_screen_done.png')
        screen.blit(activeScreen.image, activeScreen.rect)
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
            step = step + 1
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0

            # update all the sprites
            all.update()

            # draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            # cap the framerate
            clock.tick(40)

        for myScreen in myScreens:
            myScreen.kill()

        charList = [Character('Blue Crossbowman', 'blue_crossbowman.png', Rect(50, 100, 282, 440)),
                    Character('Blue Mage', 'blue_mage.png', Rect(382, 100, 282, 449)),
                    Character('Blue Sorcerer', 'blue_sorcerer.png', Rect(714, 100, 269, 500)),
                    Character('Dark Archer', 'dark_archer.png', Rect(1033, 100, 282, 374))]

        # Box
        box_rect = Rect(550, 668, 300, 90)
        box = Box(box_rect)

        # Create TextInput-object
        textinput = TextInput()
        textinput.set_text_color((255, 255, 255))

        # character selection screen
        GameData.gamestate = "character selection"
        activeScreen.setImage('character_selection.png')

        char_name = ""
        waiting = True
        response = None
        while waiting:

            screen.blit(activeScreen.image, activeScreen.rect)

            collide_list = []
            for char in charList:
                collide_list.append(screen.blit(char.image, char.rect))
                if char.name == char_name:
                    screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (134, 173, 154)),
                        (char.rect.x + 80, char.rect.height + 130))
                else:
                    screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (255, 255, 255)),
                        (char.rect.x + 80, char.rect.height + 130))

            screen.blit(box.image, box_rect)

            textSurface = Text.loadText('Enter your nickname', 'Comic Sans MS', 20, (255, 255, 255))
            screen.blit(textSurface, (box_rect.x + 70, box_rect.y + 15))

            screen.blit(textinput.get_surface(), (box_rect.x + 70, box_rect.y + 50))

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
                    response = requests.post('https://team-b-api.herokuapp.com/api/login/', json=payload)
                    waiting = False
            step = step + 1
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0

            # update all the sprites
            all.update()

            pygame.display.update()

            # cap the framerate
            clock.tick(40)

        for myScreen in myScreens:
            myScreen.kill()

        # character selection screen
        GameData.gamestate = "in game"
        activeScreen.setImage(response.json()['scenario'])

        waiting = True
        while waiting:

            screen.blit(activeScreen.image, activeScreen.rect)

            # get input
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            keystate = pygame.key.get_pressed()
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                waiting = False
            step = step + 1
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0

            # update all the sprites
            all.update()

            pygame.display.update()

            # cap the framerate
            clock.tick(int(response.json()['difficulty']))

        for myScreen in myScreens:
            myScreen.kill()

if __name__ == '__main__':
    main()

