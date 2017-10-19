import events
import string
import gui_widget
import source
import gui
import pygame
from pygame.locals import *


# ------------------------------------------------------------------------------
class SelectCharactorGUIController(gui.GUIController):
    """..."""

    def __init__(self, ev_manager):
        gui.GUIController.__init__(self, ev_manager)

    # ----------------------------------------------------------------------
    def wants_event(self, event):
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return 1

        return 0

    # ----------------------------------------------------------------------
    def handle_pygame_event(self, event):
        ev = None

        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            ev = events.QuitEvent()
        elif pygame.key.get_pressed()[K_SPACE]:
            ev = events.GUIChangeScreenRequest('ingame')

        if ev:
            self.ev_manager.post(ev)


# ------------------------------------------------------------------------------
class SelectCharactorGUIView(gui.GUIView):
    """..."""

    def __init__(self, ev_manager, render_group, rect):
        gui.GUIView.__init__(self, ev_manager, render_group, rect)

    # ----------------------------------------------------------------------
    def get_background_blit(self):
        bg_img = source.Graphics.load_background('character_selection.png')
        self.rect = bg_img.get_rect(center=source.GameData.Game.get_instance().screenrect.center)
        return [bg_img, self.rect]

    # ----------------------------------------------------------------------
    def notify(self, event):
        gui.GUIView.notify(self, event)