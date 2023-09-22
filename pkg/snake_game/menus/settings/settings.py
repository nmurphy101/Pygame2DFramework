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
    MENU_PAUSE,
    MENU_SETTINGS,
)


def settings_menu(self):
    """settings_menu

    settings_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_SETTINGS

    # Check settings if just left settings page
    if self.prev_menu not in (MENU_PAUSE, MENU_SETTINGS):
        self.game.settings_checks()

    # Render the Settings Menu text
    _ = self.render_button("Settings", 10, color=COLOR_RED)

    # Render the display button
    display_obj = self.render_button("Display", 1)

    # Render the Sound button
    sound_obj = self.render_button("Sound", -1)

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    menu = [
        (display_obj, self.display_menu, 2),
        (sound_obj, self.sound_menu, 2),
        (back_obj, self.game_menus[self.root_menu], 2),
    ]

    self.prev_menu = 2

    return menu
