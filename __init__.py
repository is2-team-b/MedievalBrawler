import source

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

