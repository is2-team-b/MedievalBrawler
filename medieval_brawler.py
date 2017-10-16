import gui
import events
import pygame
import models
import screens
import layered_group
from pygame.locals import *
from weakref import WeakKeyDictionary


def debug(msg):
    print(msg)


# ------------------------------------------------------------------------------
class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    # ----------------------------------------------------------------------
    def register_listener(self, listener):
        self.listeners[listener] = 1

    # ----------------------------------------------------------------------
    def unregister_listener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    # ----------------------------------------------------------------------
    def post(self, event):
        if not isinstance(event, events.TickEvent):
            debug("     Message: " + event.name)
        for listener in self.listeners:
            # NOTE: If the weakref has died, it will be
            # automatically removed, so we don't have
            # to worry about it.
            listener.notify(event)


#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.RegisterListener( self )

        self.keepGoing = 1

    #----------------------------------------------------------------------
    def run(self):
        if not self.keepGoing:
            raise Exception('dead spinner')
        while self.keepGoing:
            event = events.TickEvent()
            self.ev_manager.post(event)

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            #this will stop the while loop from running
            self.keepGoing = 0

class PygameMasterController:
    """..."""
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)

        #subcontrollers is an ordered list, the first controller in the
        # list is the first to be offered an event
        self.subcontrollers = []

        self.guiClasses = { 'splash': [gui.SimpleGUIController],
                            'select_charactor': [gui.SimpleGUIController],
                            'ingame': [gui.SimpleGUIController]
                          }
        self.switch_controller('splash')

    # ----------------------------------------------------------------------
    def switch_controller(self, key):

        if not self.guiClasses.has_key(key):
            raise NotImplementedError

        self.subcontrollers = []

        for contClass in self.guiClasses[key]:
            new_controller = contClass(self.ev_manager)
            self.subcontrollers.append(new_controller)


    #----------------------------------------------------------------------
    def notify(self, incoming_event):

        if isinstance(incoming_event, events.TickEvent):
            #Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = events.QuitEvent()
                    self.ev_manager.post(ev)

                elif event.type == KEYDOWN \
                  or event.type == MOUSEBUTTONUP \
                  or event.type == MOUSEMOTION:
                    for cont in self.subcontrollers:
                        if cont.wants_event(event):
                            cont.handle_pygame_event(event)
                            break

        elif isinstance(incoming_event, events.GUIChangeScreenRequest):
            self.switch_controller(incoming_event.key)


# ------------------------------------------------------------------------------
class PygameMasterView(EventManager):
    """..."""
    def __init__(self, ev_manager):
        EventManager.__init__(self)
        self.normalListeners = self.listeners
        self.dialogListeners = WeakKeyDictionary()
    
        self.ev_manager = ev_manager
        self.ev_manager.register_listener( self )
    
        pygame.init()
        self.window = pygame.display.set_mode( (440,480) )
        pygame.display.set_caption( 'Fool The Bar' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( (0,0,0) )
    
        self.window.blit( self.background, (0,0) )
        pygame.display.flip()
    
        self.dialog = None
    
        self.subviews = []
        self.sprite_group = layered_group.LayeredSpriteGroup()
    
        self.guiClasses = {'splash': [screens.SplashGUIView], 'select_charactor': [screens.SelectCharactorGUIView],
                           'ingame': [screens.InGameGUIView]}
        # the subviews that make up the current screen.  In order from
        # bottom to top
        # self.subviews = []
        
        self.switch_view('splash')

    # ----------------------------------------------------------------------
    def debug(self, ev):
        return

    # ----------------------------------------------------------------------
    def post(self, event):
        self.ev_manager.post(event)

    # ----------------------------------------------------------------------
    def switch_view(self, key):
        if self.dialog:
            raise Exception('cannot switch view while dialog up')

        if not self.guiClasses.has_key(key):
            raise NotImplementedError('master view doesnt have key')

        for view in self.subviews:
            view.kill()
        self.subviews = []

        self.sprite_group.empty()

        rect = pygame.Rect((0, 0), self.window.get_size())

        # construct the new master View
        for viewClass in self.guiClasses[key]:
            if hasattr(viewClass, 'clipRect'):
                rect = viewClass.clipRect
            view = viewClass(self, self.sprite_group, rect)
            bgBlit = view.get_background_blit()
            self.background.blit(bgBlit[0], bgBlit[1])
            self.subviews.append(view)

        # initial blit & flip of the newly constructed background
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    # ----------------------------------------------------------------------
    def handle_tick(self):
        # Clear, Update, and Draw Everything
        self.sprite_group.clear(self.window, self.background)

        self.sprite_group.update()

        dirtyRects = self.sprite_group.draw(self.window)

        pygame.display.update(dirtyRects)

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.GUIChangeScreenRequest):
            self.switch_view(event.key)

        elif isinstance(event, events.TickEvent):
            self.handle_tick()

        # at the end, handle the event like an EventManager should
        EventManager.post(self, event)


# ------------------------------------------------------------------------------
def main():
    """..."""
    ev_manager = EventManager()

    spinner = CPUSpinnerController(ev_manager)
    pygameView = PygameMasterView(ev_manager)
    pygameCont = PygameMasterController(ev_manager)
    game = models.Game(ev_manager)

    while 1:
        try:
            spinner.run()
        except NotImplementedError as e:
            text = "Not Implemented: " + str(e.strerror)
            ev = events.ExceptionEvent(text)
            ev_manager.post(ev)
        else:
            break


if __name__ == "__main__":
    main()