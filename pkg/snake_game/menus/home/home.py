#!/usr/bin/env python3

"""
    Home Menu

    Game Home menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from ...constants import game_constants


def home_menu(self):
    """home_menu

    home_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = game_constants.MENU_HOME
    self.root_menu = game_constants.MENU_HOME

    # Check settings if just left settings page

    if self.prev_menu == game_constants.MENU_PAUSE:
        # Clear game objects up to free memory
        self.game.clean_up()

    elif self.prev_menu not in [game_constants.MENU_PAUSE, game_constants.MENU_SETTINGS]:
        # Check the settings
        self.game.settings_checks()
        # just to prevent a check settings inf. loop
        self.prev_menu = game_constants.MENU_SETTINGS

    # Render the Home Menu text
    _ = self.render_button("Home Menu", 8, (255, 0, 0))

    # Render the play button
    play_obj = self.render_button("Play", 1)

    # Render the settings button
    settings_obj = self.render_button("Settings", -1)

    # Render the quit button
    quit_obj = self.render_button("Quit", -3)

    menu = [
        (play_obj, self.game.start, 0),
        (settings_obj, self.settings_menu, 0),
        (quit_obj, self.game.quit_game, 0),
    ]

    return menu
