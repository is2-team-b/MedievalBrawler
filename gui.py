import events
import string
import gui_widget
from pygame.locals import *


# ------------------------------------------------------------------------------
class GUIController:
    """..."""
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)

    # ----------------------------------------------------------------------
    def handle_pygame_event(self, event):
        """is given a pygame.event and is responsible for generating
        an event defined in the local events module, or doing nothing"""
        pass

    # ----------------------------------------------------------------------
    def notify(self, event):
        pass
    
    
# ------------------------------------------------------------------------------
class SimpleGUIController(GUIController):
    """..."""
    # ----------------------------------------------------------------------
    def wants_event(self, event):
        if event.type == KEYDOWN \
          or event.type == MOUSEBUTTONUP \
          or event.type == MOUSEMOTION:
            return 1
    
        return 0

    # ----------------------------------------------------------------------
    def handle_pygame_event(self, event):
        ev = None
    
        if event.type == KEYDOWN \
             and event.key == K_ESCAPE:
            ev = events.QuitEvent()
    
        elif event.type == KEYDOWN \
             and event.key == K_UP:
            ev = events.GUIFocusPrevWidgetEvent()
    
        elif event.type == KEYDOWN \
             and event.key == K_DOWN:
            ev = events.GUIFocusNextWidgetEvent()
    
        elif event.type == KEYDOWN \
             and (event.key == K_RETURN
             or event.key == K_SPACE):
            ev = events.GUIPressEvent()
    
        elif event.type == KEYDOWN :
            character = str(event.unicode)
            if character and character in string.printable:
                ev = events.GUIKeyEvent(character)
            elif event.key == K_BACKSPACE:
                ev = events.GUIControlKeyEvent(event.key)

        elif event.type == MOUSEBUTTONUP:
            b = event.button
            if b == 1:
                ev = events.GUIClickEvent(event.pos)
    
        elif event.type == MOUSEMOTION:
            ev = events.GUIMouseMoveEvent(event.pos)

        if ev:
            self.ev_manager.post(ev)


# ------------------------------------------------------------------------------
class GUIView(gui_widget.WidgetContainer):
    """..."""
    def __init__( self, ev_manager, render_group, rect):
        gui_widget.WidgetContainer.__init__(self, ev_manager, rect)
    
        self.render_group = render_group