#!/usr/bin/env python3

"""
    Settings Menu

    The settings menu with options for different settings menus

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_DISPLAY,
    MENU_GAMEPLAY,
    MENU_KEYBINDING,
    MENU_PAUSE,
    MENU_SOUND,
    MENU_SETTINGS,
)


def settings_menu(self):
    """settings_menu

    settings_menu does stuff
    """

    # Clear previous frame render
    self.app.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_SETTINGS

    # Render the Settings Menu text
    _ = self.render_button("Settings", 10, color=COLOR_RED)

    # Render the display button
    display_obj = self.render_button("Display", 5)

    # Render the Sound button
    sound_obj = self.render_button("Sound", 3)

    # Render the Sound button
    gameplay_obj = self.render_button("Gameplay", 1)

    # Render the Sound button
    keybinding_obj = self.render_button("Keybinding", -1)

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    menu = [
        (display_obj, self.menu_options[MENU_DISPLAY], 2),
        (sound_obj, self.menu_options[MENU_SOUND], 2),
        (gameplay_obj, self.menu_options[MENU_GAMEPLAY], 2),
        (keybinding_obj, self.menu_options[MENU_KEYBINDING], 2),
        (back_obj, self.menu_options[self.root_menu], 2),
    ]

    self.prev_menu = 2

    return menu
