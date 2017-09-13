# GameData : this module contains all global constants & variables

from pygame.locals import *

screenrect = Rect(0, 0, 1366, 768)      # constant: complete window
arenarect = Rect(0, 0, 1366, 768)       # constant: part of window to play in
animstep = 0                           # variable: animation cycle

gamestate = "splash screen"            # variable