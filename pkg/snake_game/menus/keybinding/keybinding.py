#!/usr/bin/env python3

"""
    Keybinding Menu

    Keybinding settings menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    MENU_KEYBINDING,
)


def keybinding_menu(self):
    """keybinding_menu

    keybinding_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_KEYBINDING

    # Render the Display text
    self.render_button("Keybindings", 10, color=COLOR_RED)

    # initilize menu
    menu = []

    # Render the Return button
    back_obj = self.render_button("Back", -8)
    menu.append((back_obj, self.settings_menu, 6))

    # Render all the keybinding buttons
    keybindings = self.game.game_config["settings"]["keybindings"]

    index = 4
    for action, key in keybindings.items():
        _ = self.render_button(f"{action.replace('_', ' ')}:", index, h_offset=-110, w_offset=20)
        button = self.render_button(key, index, color=COLOR_PURPLE, h_offset=145, w_offset=20)
        menu.append((button, self.change_keybinding, self.prev_menu, action))
        index -= 1.5

    return menu
