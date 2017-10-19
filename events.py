class Event:
    """
    this is a superclass for any events that might be generated by an
    object and sent to the EventManager
    """

    def __init__(self):
        self.name = "Generic Event"


class TickEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.name = "CPU Tick Event"


class QuitEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.name = "Program Quit Event"


class MapBuiltEvent(Event):
    def __init__(self, gameMap):
        Event.__init__(self)
        self.name = "Map Finished Building Event"
        self.map = gameMap


class GameStartedEvent(Event):
    def __init__(self, game):
        Event.__init__(self)
        self.name = "Game Started Event"
        self.game = game


class CharactorMoveRequest(Event):
    def __init__(self, direction):
        Event.__init__(self)
        self.name = "Charactor Move Request"
        self.direction = direction


class CharactorPlaceEvent(Event):
    """this event occurs when a Charactor is *placed* in a sector,
    ie it doesn't move there from an adjacent sector."""

    def __init__(self, charactor):
        Event.__init__(self)
        self.name = "Charactor Placement Event"
        self.charactor = charactor


class CharactorMoveEvent(Event):
    def __init__(self, charactor):
        Event.__init__(self)
        self.name = "Charactor Move Event"
        self.charactor = charactor


class GUIFocusNextWidgetEvent(Event):
    """..."""

    def __init__(self, layer=0):
        Event.__init__(self)
        self.name = "Activate the next widget Event"
        self.layer = layer


class GUIFocusPrevWidgetEvent(Event):
    """..."""

    def __init__(self, layer=0):
        Event.__init__(self)
        self.name = "Activate the previous widget Event"
        self.layer = layer


class GUIFocusThisWidgetEvent(Event):
    """..."""

    def __init__(self, widget):
        Event.__init__(self)
        self.name = "Activate particular widget Event"
        self.widget = widget


class GUIPressEvent(Event):
    """..."""

    def __init__(self, layer=0):
        Event.__init__(self)
        self.name = "All Active widgets get pressed Event"
        self.layer = layer


class GUIKeyEvent(Event):
    """..."""

    def __init__(self, key, layer=0):
        Event.__init__(self)
        self.name = "key pressed Event"
        self.key = key
        self.layer = layer


class GUIControlKeyEvent(Event):
    """..."""

    def __init__(self, key):
        Event.__init__(self)
        self.name = "Non-Printablekey pressed Event"
        self.key = key


class GUIClickEvent(Event):
    """..."""

    def __init__(self, pos, layer=0):
        Event.__init__(self)
        self.name = "Mouse Click Event"
        self.pos = pos
        self.layer = layer


class GUIMouseMoveEvent(Event):
    """..."""

    def __init__(self, pos, layer=0):
        Event.__init__(self)
        self.name = "Mouse Moved Event"
        self.pos = pos
        self.layer = layer


class GUICharactorSelectedEvent(Event):
    """..."""

    def __init__(self, charactor, wipeOthers=1):
        Event.__init__(self)
        self.name = "A Charactor has been selected by the user"
        self.charactor = charactor
        self.wipeOthers = wipeOthers


class GUICharactorUnSelectedEvent(Event):
    """..."""

    def __init__(self, charactor):
        Event.__init__(self)
        self.name = "A Charactor has been unselected by the user"
        self.charactor = charactor


class GUIChangeScreenRequest(Event):
    """..."""

    def __init__(self, key):
        Event.__init__(self)
        self.name = "Change the active GUI to the one referenced by key"
        self.key = key


class GameSyncEvent(Event):
    """..."""
    def __init__(self, game):
        Event.__init__(self)
        self.name = "Game Synched to Authoritative State"
        self.game = game


class ExceptionEvent(Event):
    """..."""

    def __init__(self, msg):
        Event.__init__(self)
        self.name = "An exception occurred that we can handle"
        self.msg = msg