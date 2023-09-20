#!/usr/bin/env python3

"""
    Settings Menu

    The settings menu with options for different settings menus

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


def settings_menu(self):
    """settings_menu

    settings_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 2

    # Check settings if just left settings page
    if self.prev_menu not in (1, 2):
        self.game.settings_checks()

    # Render the Settings Menu text
    _ = self.render_button("Settings", 10, (255, 0, 0))

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
