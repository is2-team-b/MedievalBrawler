import gui
import gui_widget
import events
import pygame

# ------------------------------------------------------------------------------
class SplashGUIView(gui.GUIView):
    """..."""

    def __init__(self, ev_manager, render_group, rect):
        gui.GUIView.__init__(self, ev_manager, render_group, rect)

        # quitEvent = events.QuitEvent()
        # optEvent = events.GUIChangeScreenRequest('splash')
        # playEvent = events.GameStartRequest()
            
        screen = gui_widget.MyScreen(ev_manager, 'splash_screen_done.png', container=self)
        
        self.widgets = [screen]

        self.render_group.add(self.widgets)

    # ----------------------------------------------------------------------
    def get_background_blit(self):
        bgImg = pygame.Surface((self.rect.width, self.rect.height))
        bgImg.fill((0, 100, 0))
        return [bgImg, self.rect]

    # ----------------------------------------------------------------------
    def notify(self, event):
        gui.GUIView.notify(self, event)

        if isinstance(event, events.GameStartedEvent):
            ev = events.GUIChangeScreenRequest('select_charactor')
            self.ev_manager.post(ev)


# ------------------------------------------------------------------------------
class SelectCharactorGUIView(gui.GUIView):
    """..."""

    def __init__(self, ev_manager, render_group, rect):
        gui.GUIView.__init__(self, ev_manager, render_group, rect)

        # quitEvent = events.QuitEvent()
        # optEvent = events.GUIChangeScreenRequest('splash')
        # playEvent = events.GameStartRequest()

        screen = gui_widget.MyScreen(ev_manager, 'character_selection.png', container=self)

        self.widgets = [screen]

        self.render_group.add(self.widgets)

    # ----------------------------------------------------------------------
    def get_background_blit(self):
        bgImg = pygame.Surface((self.rect.width, self.rect.height))
        bgImg.fill((0, 100, 0))
        return [bgImg, self.rect]

    # ----------------------------------------------------------------------
    def notify(self, event):
        gui.GUIView.notify(self, event)

        if isinstance(event, events.GameStartedEvent):
            ev = events.GUIChangeScreenRequest('ingame')
            self.ev_manager.post(ev)


# ------------------------------------------------------------------------------
class InGameGUIView(gui.GUIView):
    """..."""

    def __init__(self, ev_manager, render_group, rect, scenario):
        gui.GUIView.__init__(self, ev_manager, render_group, rect)

        # quitEvent = events.QuitEvent()
        # optEvent = events.GUIChangeScreenRequest('splash')
        # playEvent = events.GameStartRequest()

        screen = gui_widget.MyScreen(ev_manager, scenario, container=self)

        self.widgets = [screen]

        self.render_group.add(self.widgets)

    # ----------------------------------------------------------------------
    def get_background_blit(self):
        bgImg = pygame.Surface((self.rect.width, self.rect.height))
        bgImg.fill((0, 100, 0))
        return [bgImg, self.rect]