#!/usr/bin/env python3

"""
    Home Menu

    Game Home menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from pkg.menus import Menu

from pkg.games.snake_game.constants.game_constants import (
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

    if self.refresh or self.menu_option != MENU_HOME or not self.prev_menu:
        # Clear previous frame render
        self.app.game.screen.fill(COLOR_BLACK)

        # Make sure the right menu option is selected
        self.menu_option = MENU_HOME

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
        self.render_text(GAME_TITLE, 8, color=COLOR_RED)

        # Render the play button
        play_obj = self.render_button("Play", 2, has_outline=True)

        # Render the leaderboard button
        leaderboard_obj = self.render_button("Leaderboard", 0, has_outline=True)

        # Render the settings button
        settings_obj = self.render_button("Settings", -2, has_outline=True)

        # Render the quit button
        quit_obj = self.render_button("Quit", -4, has_outline=True)

        self.menu = [
            (play_obj, self.app.game.start, MENU_HOME, None),
            (leaderboard_obj, self.menu_options[MENU_LEADERBOARD], MENU_HOME, None),
            (settings_obj, self.menu_options[MENU_SETTINGS], MENU_HOME, None),
            (quit_obj, self.app.game.quit_game, MENU_HOME, None),
        ]

        self.refresh = False

    return self.menu
