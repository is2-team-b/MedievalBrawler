import os.path

import pygame
from pygame.locals import *
import requests

from source import GameData, Graphics   # contains all global variables
from source import SelectChar           # Character selection screen class
from source import SplashScreen         # Splash screen class
from source import GameOver             # Game Over screen class
from source import Character            # Character class
from source import Box
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
    SplashScreen.image = Graphics.load_image('splash_screen_done.png')
    SelectChar.image = Graphics.load_image('character_selection.png')
    GameOver.images = [Graphics.load_image('game_over.jpg')]
    #Character.images = Graphics.load_images('blue_crossbowman.png', 'blue_mage.png', 'blue_sorcerer.png', 'dark_archer.png')

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
    splashscreens = pygame.sprite.Group()
    gameovers = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    SplashScreen.containers = splashscreens, all
    SelectChar.containers = splashscreens, all
    GameOver.containers = gameovers, all
    Character.containers = characters, all
    Box.containers = boxes, all

    step = 0  # used in calculation of animation cycles

    # main loop
    while True:
        # splash screen
        GameData.gamestate = "splash screen"
        active_screen = SplashScreen()

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

            # clear/erase the last drawn sprites
            all.clear(screen, background)

            # draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            # cap the framerate
            clock.tick(40)

        for splashscreen in splashscreens:
            splashscreen.kill()

        # character selection screen
        GameData.gamestate = "character selection"
        active_screen = SelectChar()
        screen.blit(background, (0, 0))
        charList = [Character('Blue Crossbowman', 'blue_crossbowman.png', Rect(50, 100, 282, 440)),
                    Character('Blue Mage', 'blue_mage.png', Rect(382, 100, 282, 449)),
                    Character('Blue Sorcerer', 'blue_sorcerer.png', Rect(714, 100, 269, 500)),
                    Character('Dark Archer', 'dark_archer.png', Rect(1033, 100, 282, 374))]
        collide_list = []
        for char in charList:
            collide_list.append(screen.blit(char.image, char.rect))

        #Box
        box_rect = Rect(433, 600, 400, 150)
        box = Box(box_rect)
        screen.blit(box.image, box_rect)

        waiting = True
        while waiting:
            # Create TextInput-object
            textinput = TextInput()
            textinput.set_text_color((255, 255, 255))
            events = pygame.event.get()
            # Feed it with events every frame
            textinput.update(events)
            screen.blit(textinput.get_surface(), (box_rect.x + 63, box_rect.y + 25))
            # draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)
            # cap the framerate
            clock.tick(40)

            mousestate = False
            # get input
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mousestate = True
                    break
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    break
            myfont = pygame.font.SysFont('Comic Sans MS', 14)
            textsurface = myfont.render('', False, (255, 255, 255))
            if mousestate:
                mouse_pos = pygame.mouse.get_pos()
                i = 0
                for char in charList:
                    if collide_list[i].collidepoint(mouse_pos):
                        textsurface = myfont.render(char.name, False, (255, 255, 255))
                        payload = {'name': char.name}
                        requests.post('https://team-b-api.herokuapp.com/api/user/', json=payload)
                        break
                    i += 1
                screen.blit(textsurface, (box_rect.x, box_rect.height - 65))
                # draw the scene
                dirty = all.draw(screen)
                pygame.display.update(dirty)
                # cap the framerate
                clock.tick(40)
            keystate = pygame.key.get_pressed()
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                waiting = False
                print(str(textinput.get_text().__len__()))
            step = step + 1
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0

            # clear/erase the last drawn sprites
            all.clear(screen, background)
            # Feed it with events every frame
            textinput.update(events)

            # draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)
            # cap the framerate
            clock.tick(40)

        for splashscreen in splashscreens:
            splashscreen.kill()

        GameData.gamestate = "gameover"
        active_screen = GameOver()
        screen.blit(background, (0, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
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
            # clear/erase the last drawn sprites
            all.clear(screen, background)
            # draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)
            # cap the framerate
            clock.tick(40)
        for gameover in gameovers:
            gameover.kill()

if __name__ == '__main__':
    main()

