#!/usr/bin/env python3

"""
    Settings Menu

    The settings menu with options for different settings menus

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from pkg.menus import Menu

from pkg.games.snake_game.constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_DISPLAY,
    MENU_GAMEPLAY,
    MENU_KEYBINDING,
    MENU_HOME,
    MENU_PAUSE,
    MENU_SOUND,
    MENU_SETTINGS,
)


def settings_menu(self: Menu):
    """settings_menu

    settings_menu does stuff
    """

    if self.refresh or self.menu_option != MENU_SETTINGS:
        # Clear previous frame render
        self.app.screen.fill(COLOR_BLACK)

        # Make sure the right menu option is selected
        self.menu_option = MENU_SETTINGS

        if self.prev_menu in [MENU_HOME, MENU_PAUSE]:
            self.root_menu = self.prev_menu

        # Render the Settings Menu text
        self.render_text("Settings", 10, color=COLOR_RED)

        # Render the display button
        display_obj = self.render_button("Display", 5, has_outline=True)

        # Render the Sound button
        sound_obj = self.render_button("Sound", 3, has_outline=True)

        # Render the Sound button
        gameplay_obj = self.render_button("Gameplay", 1, has_outline=True)

        # Render the Sound button
        keybinding_obj = self.render_button("Keybinding", -1, has_outline=True)

        # Render the Return button
        back_obj = self.render_button("Back", -8, has_outline=True)

        self.menu = [
            (display_obj, self.menu_options[MENU_DISPLAY], MENU_SETTINGS, None),
            (sound_obj, self.menu_options[MENU_SOUND], MENU_SETTINGS, None),
            (gameplay_obj, self.menu_options[MENU_GAMEPLAY], MENU_SETTINGS, None),
            (keybinding_obj, self.menu_options[MENU_KEYBINDING], MENU_SETTINGS, None),
            (back_obj, self.menu_options[self.root_menu], MENU_SETTINGS, None),
        ]

        self.refresh = False

    return self.menu
