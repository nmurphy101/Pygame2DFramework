#!/usr/bin/env python3

"""
    Home Menu

    Game Home menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from .....menus import Menu

from ...constants.game_constants import (
    GAME_TITLE,
    COLOR_BLACK,
    COLOR_RED,
    MENU_HOME,
    MENU_PAUSE,
    MENU_GAME_OVER,
    MENU_LEADERBOARD,
    MENU_SETTINGS,
)


def home_menu(self: Menu):
    """home_menu

    home_menu does stuff
    """

    # Clear previous frame render
    self.app.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_HOME
    self.root_menu = MENU_HOME

    # Check settings if just left settings page
    if self.prev_menu in [MENU_PAUSE, MENU_GAME_OVER]:
        # Clear game objects up to free memory
        self.app.game.clean_up()

    elif self.prev_menu not in [MENU_PAUSE, MENU_SETTINGS]:
        # Check the settings
        self.app.settings_checks()
        # just to prevent a check settings inf. loop
        self.prev_menu = MENU_SETTINGS

    # Render the Home Menu text
    _ = self.render_button(GAME_TITLE, 8, color=COLOR_RED)

    # Render the play button
    play_obj = self.render_button("Play", 1)

    # Render the leaderboard button
    leaderboard_obj = self.render_button("Leaderboard", -1)

    # Render the settings button
    settings_obj = self.render_button("Settings", -3)

    # Render the quit button
    quit_obj = self.render_button("Quit", -5)

    menu = [
        (play_obj, self.app.game.start, 0),
        (leaderboard_obj, self.menu_options[MENU_LEADERBOARD], 0),
        (settings_obj, self.menu_options[MENU_SETTINGS], 0),
        (quit_obj, self.app.game.quit_game, 0),
    ]

    return menu
