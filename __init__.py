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

    # splashScreen = MyScreen(Graphics.load_background('splash_screen_done.png'))
    # selectCharScreen = MyScreen(Graphics.load_background('character_selection.png'))
    # gameOverScreen = MyScreen(Graphics.load_background('game_over.jpg'))

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
    # texts = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    #
    # assign default groups to each sprite class
    MyScreen.containers = myScreens, all
    # SelectChar.containers = screens, all
    # GameOver.containers = screens, all
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

            # clear/erase the last drawn sprites
            all.clear(screen, activeScreen.image)

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

        char_name = ""
        waiting = True
        while waiting:
            # # Create TextInput-object
            # textinput = TextInput()
            # textinput.set_text_color((255, 255, 255))
            # events = pygame.event.get()
            # # Feed it with events every frame
            # textinput.update(events)
            # screen.blit(textinput.get_surface(), (box_rect.x + 63, box_rect.y + 25))
            # # draw the scene
            # dirty = all.draw(screen)
            # pygame.display.update(dirty)
            # # cap the framerate
            # clock.tick(40)

            # character selection screen
            GameData.gamestate = "character selection"
            activeScreen.setImage('character_selection.png')
            screen.blit(activeScreen.image, activeScreen.rect)
            myScreens.update()
            # draw the scene
            myScreens.draw(screen)

            collide_list = []
            for char in charList:
                collide_list.append(screen.blit(char.image, char.rect))
                if char.name == char_name:
                    screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (134, 173, 154)),
                            (char.rect.x + 80, char.rect.height + 130))
                else:
                    screen.blit(Text.loadText(char.name, 'Comic Sans MS', 20, (255, 255, 255)),
                            (char.rect.x + 80, char.rect.height + 130))
            characters.update()
            characters.draw(screen)

            screen.blit(box.image, box_rect)
            boxes.update()
            boxes.draw(screen)

            textSurface = Text.loadText(char_name, 'Comic Sans MS', 20, (255, 255, 255))
            screen.blit(textSurface, (box_rect.x + 70, box_rect.y + 15))

            pygame.display.update()

            mousestate = False
            # get input
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mousestate = True
                    break
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    break

            if mousestate:
                mouse_pos = pygame.mouse.get_pos()
                i = 0
                for char in charList:
                    if collide_list[i].collidepoint(mouse_pos):
                        char_name = char.name
                        payload = {'name': char.name}
                        requests.post('https://team-b-api.herokuapp.com/api/user/', json=payload)
                        break
                    i += 1

            keystate = pygame.key.get_pressed()
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                waiting = False
                # print(str(textinput.get_text().__len__()))
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

            # clear/erase the last drawn sprites
            # all.clear(textSurface, (box_rect.x + 150, box_rect.y + 65))
            # active_screen.update()
            # # Feed it with events every frame
            # # textinput.update(events)
            # # draw the scene
            # dirty = all.draw(textSurface)
            # pygame.display.update(dirty)
            # # cap the framerate
            # clock.tick(40)

        for myScreen in myScreens:
            myScreen.kill()

        GameData.gamestate = "gameover"
        activeScreen = GameOver()
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

if __name__ == '__main__':
    main()

