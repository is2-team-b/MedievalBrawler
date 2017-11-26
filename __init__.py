import source
from source.state.state_init_sound import StateInitSound
from source.state.state_init_screen import StateInitScreen
from source.state.state_loaded_sound import StateLoadedSound
from source.state.state_created_groups import StateCreatedGroups
from source.state.state_assigned_to_groups import StateAssignedToGroups
from source.state.state_splash_screen import StateSplashScreen
from source.state.state_char_selection_screen import StateCharSelectionScreen
from source.state.state_ingame_screen import StateIngameScreen
from source.state.state_victory_screen import StateVictoryScreen
from source.state.state_match_completed_screen import StateMatchCompletedScreen
from source.state.state_game_over_screen import StateGameOverScreen

# Classes
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# Functions
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------


def main():
    source.GameData.Game.get_instance().state.init_sound()
    source.GameData.Game.get_instance().state.init_screen()
    source.GameData.Game.get_instance().state.load_sound()
    source.GameData.Game.get_instance().state.create_groups()
    source.GameData.Game.get_instance().state.assign_to_groups()

    # main loop
    source.GameData.Game.get_instance().state.show_splash_screen()
    source.GameData.Game.get_instance().state.show_char_selection_screen()

    source.GameData.Game.get_instance().state.show_ingame_screen()
    source.GameData.Game.get_instance().state.show_stage_result_screen()

    source.GameData.Game.get_instance().state.show_ingame_screen()
    source.GameData.Game.get_instance().state.show_stage_result_screen()

    source.GameData.Game.get_instance().state.show_match_completed_screen()

    source.GameData.Game.get_instance().state.show_game_over_screen()


if __name__ == '__main__':
    main()

