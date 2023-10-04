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
    MENU_SETTINGS,
    MENU_GAMEPLAY,
)


def gameplay_menu(self):
    """gameplay_menu

    gameplay_menu does stuff
    """

    # Clear previous frame render
    self.app.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_GAMEPLAY

    # Render the Display text
    self.render_button("Gameplay", 10, color=COLOR_RED)

    # initilize menu
    menu = []

    # Render the Save button
    save_obj = self.render_button("Save", -8, h_offset=125)
    menu.append((save_obj, self.save_settings, self.prev_menu))

    # Render the Return button
    back_obj = self.render_button("Back", -8, h_offset=-125)
    menu.append((back_obj, self.menu_options[MENU_SETTINGS], self.prev_menu))

    # Render all the gameplay buttons
    gameplay_config = self.app.game.game_config["settings"]["gameplay"]

    index = 8
    row_mod = -300
    count = 0
    largest_setting_len = len(max(gameplay_config.keys(), key = len))
    for setting, value in gameplay_config.items():
        if count > 6:
            count = 0
            row_mod = row_mod * -1
            index = 8

        if isinstance(value, bool):
            padding = largest_setting_len - len(setting)
            _ = self.render_button(f"{padding*' '}{setting.replace('_', ' ')}:", index, h_offset=row_mod-110, w_offset=20)
            button = self.render_button(value, index, color=COLOR_PURPLE, h_offset=(row_mod+175), w_offset=20)
            menu.append((button, self.toggle_gameplay_setting, self.prev_menu, setting))

        elif isinstance(value, int) or isinstance(value, float):
            padding = largest_setting_len - len(setting)
            _ = self.render_button(f"{padding*' '}{setting.replace('_', ' ')}:", index, h_offset=row_mod-110, w_offset=20)
            _ = self.render_button(value, index, color=COLOR_PURPLE, h_offset=(row_mod+155), w_offset=20)
            index -= 1.5
            # Render the Volume Up button
            up_obj = self.render_button("Up", index, color=COLOR_PURPLE, w_offset=10, h_offset=row_mod+50)
            menu.append((up_obj,  self.increase_gameplay_setting, self.prev_menu, setting))
            # Render the Volume Down button
            down_obj = self.render_button("Down", index, color=COLOR_PURPLE, w_offset=10, h_offset=row_mod-100)
            menu.append((down_obj, self.decrease_gameplay_setting, self.prev_menu, setting))

        index -= 1.5
        count += 1

    return menu
