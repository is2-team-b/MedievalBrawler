import events

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3


# ------------------------------------------------------------------------------
class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    # ----------------------------------------------------------------------
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager
        self.ev_manager.register_listener(self)
        self.state = None
        #self.reset()

    # ----------------------------------------------------------------------
    # def reset(self):
    #     self.state = Game.STATE_PREPARING
    #
    #     self.players = []
    #     self.maxPlayers = 3
    #     self.map = Map(self.ev_manager)
    #
    #     cpuPlayer = ComputerPlayer(self.ev_manager)
    #     self.AddPlayer(cpuPlayer)

    # ----------------------------------------------------------------------
    def start(self):
        #self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = events.GameStartedEvent(self)
        self.ev_manager.post(ev)

    # ----------------------------------------------------------------------
    # def AddPlayer(self, player):
    #     self.players.append(player)
    #     player.SetGame(self)
    #     ev = PlayerJoinEvent(player)
    #     self.ev_manager.post(ev)

    # ----------------------------------------------------------------------
    def notify(self, event):
        # if isinstance(event, events.GameStartRequest):
        #     if self.state == Game.STATE_PREPARING:
        #         self.Start()
        #     elif self.state == Game.STATE_RUNNING:
        #         self.reset()
        #         self.Start()
        #
        # if isinstance(event, events.PlayerJoinRequest):
        #     if len(self.players) < self.maxPlayers:
        #         player = Player(self.ev_manager)
        #         player.SetData(event.playerDict)
        #         for p in self.players:
        #             if p.name == player.name:
        #                 # FAIL
        #                 raise NotImplementedError, "Dup Player"
        #         self.AddPlayer(player)

        if isinstance(event, events.GUIChangeScreenRequest):
            ev = events.GameSyncEvent(self)
            self.ev_manager.post(ev)