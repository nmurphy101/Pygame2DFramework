#!/usr/bin/env python3

"""
    Keybinding Menu

    Keybinding settings menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from .....menus import Menu

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    MENU_KEYBINDING,
    MENU_SETTINGS,
)


def keybinding_menu(self: Menu):
    """keybinding_menu

    keybinding_menu does stuff
    """

    if self.refresh or self.menu_option != MENU_KEYBINDING:
        # Clear previous frame render
        self.app.screen.fill(COLOR_BLACK)

        # Make sure the right menu option is selected
        self.menu_option = MENU_KEYBINDING

        # Render the Display text
        self.render_button("Keybindings", 10, color=COLOR_RED)

        # initilize menu
        menu_builder = []

        # Render the Save button
        save_obj = self.render_button("Save", -8, h_offset=125, has_outline=True)
        menu_builder.append((save_obj, self.save_settings, MENU_KEYBINDING, None))

        # Render the Return button
        back_obj = self.render_button("Back", -8, h_offset=-125, has_outline=True)
        menu_builder.append((back_obj, self.menu_options[MENU_SETTINGS], MENU_KEYBINDING, None))

        # Render all the keybinding buttons
        keybindings = self.app.game.game_config["settings"]["keybindings"]

        index = 4
        for action, key in keybindings.items():
            _ = self.render_button(f"{action.replace('_', ' ')}:", index, h_offset=-110, w_offset=20)
            button = self.render_button(key, index, color=COLOR_PURPLE, h_offset=145, w_offset=20, has_outline=True)
            menu_builder.append((button, self.change_keybinding, MENU_KEYBINDING, action))
            index -= 1.5

        self.menu = menu_builder

        self.refresh = False

    return self.menu