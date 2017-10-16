import source
import events
import pygame


# ------------------------------------------------------------------------------
class Widget(pygame.sprite.Sprite):
    def __init__(self, ev_manager, container=None):
        pygame.sprite.Sprite.__init__(self)

        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)

        self.container = container
        self.focused = 0
        self.dirty = 1

    # ----------------------------------------------------------------------
    def set_focus(self, val):
        self.focused = val
        self.dirty = 1

    # ----------------------------------------------------------------------
    def kill(self):
        self.container = None
        del self.container
        pygame.sprite.Sprite.kill(self)

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.GUIFocusThisWidgetEvent) \
          and event.widget is self:
            self.set_focus(1)

        elif isinstance(event, events.GUIFocusThisWidgetEvent) \
          and self.focused:
            self.set_focus(0)


class MyScreen(Widget):
    # The screen from which the player can start a new game
    def __init__(self, ev_manager, image, container=None):
        Widget.__init__(self, ev_manager, container)
        self.image = source.Graphics.load_background(image)
        self.rect = self.image.get_rect(center=source.GameData.Game.get_instance().screenrect.center)

    def set_image(self, image):
        self.image = source.Graphics.load_background(image)
        self.rect = self.image.get_rect(center=source.GameData.Game.get_instance().screenrect.center)
        

# ------------------------------------------------------------------------------
class WidgetContainer:
    def __init__(self, ev_manager, rect):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)
    
        self.rect = rect
    
        self.widgets = []

    # ----------------------------------------------------------------------
    def change_focused_widget(self, change):
        i = 0
        for wid in self.widgets:
            if wid.focused:
                break
            i += 1

        currently_focused = i
        change_to_widget = i + change

        # no widget was focused
        if currently_focused == len(self.widgets):
            self.widgets[0].set_focus(1)
            return

        # the desired index is out of range
        elif change_to_widget <= -1 \
                or change_to_widget >= len(self.widgets):
            change_to_widget = change_to_widget % len(self.widgets)

        self.widgets[currently_focused].set_focus(0)
        self.widgets[change_to_widget].set_focus(1)

    # ----------------------------------------------------------------------
    def notify(self, event):
    
        if isinstance(event, events.GUIFocusNextWidgetEvent):
            self.change_focused_widget(1)
    
        elif isinstance(event, events.GUIFocusPrevWidgetEvent):
            self.change_focused_widget(-1)
    
    # ----------------------------------------------------------------------
    def kill(self):
        for sprite in self.widgets:
            sprite.kill()
        while len(self.widgets) > 0:
            wid = self.widgets.pop()
            del wid
        del self.widgets