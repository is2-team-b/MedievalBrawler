import os.path
import gui
import events
import pygame
import models
import screens
import layered_group
import splash_screen
import select_charactor_screen
import source
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


# ------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)

        self.keepGoing = 1

    # ----------------------------------------------------------------------
    def run(self):
        if not self.keepGoing:
            raise Exception('dead spinner')
        while self.keepGoing:
            event = events.TickEvent()
            self.ev_manager.post(event)

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            #this will stop the while loop from running
            self.keepGoing = 0


class PygameMasterController:
    """..."""
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)

        # subcontrollers is an ordered list, the first controller in the
        # list is the first to be offered an event
        self.subcontrollers = []

        self.gui_classes = { 'splash': [splash_screen.SplashGUIController],
                            'select_charactor': [select_charactor_screen.SelectCharactorGUIController]}
        self.switch_controller('splash')

    # ----------------------------------------------------------------------
    def switch_controller(self, key):

        if key not in self.gui_classes:
            raise NotImplementedError

        self.subcontrollers = []

        for contClass in self.gui_classes[key]:
            new_controller = contClass(self.ev_manager)
            self.subcontrollers.append(new_controller)

    # ----------------------------------------------------------------------
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
    
        # Initialize pygame
        pygame.init()
        pygame.font.init()

        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        self.clock = pygame.time.Clock()
        self.screenrect = source.GameData.Game.get_instance().screenrect

        screenmode = input('(1-2) ')
        if screenmode == '1':
            bestdepth = pygame.display.mode_ok(self.screenrect.size, pygame.FULLSCREEN, 32)
            self.screen = pygame.display.set_mode(self.screenrect.size, pygame.FULLSCREEN,
                                                       bestdepth)
        else:
            self.screen = pygame.display.set_mode(self.screenrect.size)

        # decorate the game window
        pygame.mouse.set_visible(1)

        # create the background: tile the bgd image & draw the game maze
        self.background = pygame.Surface(self.screenrect.size)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # load the sound effects
        if pygame.mixer:
            self.music = os.path.join('sound', 'lvl1_invincible.mp3')
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
    
        self.dialog = None
    
        self.subviews = []
        self.sprite_group = layered_group.LayeredSpriteGroup()
    
        self.gui_classes = {'splash': [splash_screen.SplashGUIView],
                           'select_charactor': [select_charactor_screen.SelectCharactorGUIView]}
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

        if key not in self.gui_classes:
            raise NotImplementedError('master view doesnt have key')

        for view in self.subviews:
            view.kill()
        self.subviews = []

        # self.sprite_group.empty()

        rect = pygame.Rect((0, 0), self.screen.get_size())

        # construct the new master View
        for viewClass in self.gui_classes[key]:
            if hasattr(viewClass, 'clipRect'):
                rect = viewClass.clipRect
            view = viewClass(self, self.sprite_group, rect)
            bg_blit = view.get_background_blit()
            self.background.blit(bg_blit[0], bg_blit[1])
            self.subviews.append(view)

        # initial blit & flip of the newly constructed background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    # ----------------------------------------------------------------------
    def handle_tick(self):
        # lear, Update, and Draw Everything
        self.sprite_group.clear(self.screen, self.background)

        self.sprite_group.update()

        dirty_rects = self.sprite_group.draw(self.screen)

        pygame.display.update(dirty_rects)
        
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