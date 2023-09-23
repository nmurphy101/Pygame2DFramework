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

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    # Render all the keybinding buttons
    keybindings = self.game.game_config["settings"]["keybindings"]

    _ = self.render_button("Move Up:", 4, h_offset=-110, w_offset=20)
    move_up_button = self.render_button(keybindings["move_up"], 4, color=COLOR_PURPLE, h_offset=135, w_offset=20)

    _ = self.render_button("Move Left:", 2.5, h_offset=-110, w_offset=20)
    move_left_button = self.render_button(keybindings["move_left"], 2.5, color=COLOR_PURPLE, h_offset=135, w_offset=20)

    _ = self.render_button("Move Down:", 1, h_offset=-110, w_offset=20)
    move_down_button = self.render_button(keybindings["move_down"], 1, color=COLOR_PURPLE, h_offset=135, w_offset=20)

    _ = self.render_button("Move Right:", -.5, h_offset=-110, w_offset=20)
    move_right_button = self.render_button(keybindings["move_right"], -.5, color=COLOR_PURPLE, h_offset=135, w_offset=20)

    menu = [
        (move_up_button, lambda: self.change_keybinding("move_up"), self.prev_menu),
        (move_left_button, lambda: self.change_keybinding("move_left"), self.prev_menu),
        (move_down_button, lambda: self.change_keybinding("move_down"), self.prev_menu),
        (move_right_button, lambda: self.change_keybinding("move_right"), self.prev_menu),
        (back_obj, self.settings_menu, 6),
    ]

    return menu
