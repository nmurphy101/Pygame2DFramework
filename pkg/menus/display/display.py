#!/usr/bin/env python3

"""
    Display Menu

    Display settings menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from typing import TYPE_CHECKING

from ...constants.app_constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    MENU_DISPLAY,
    MENU_SETTINGS,
)

if TYPE_CHECKING:
    from ..menus import Menu


def display_menu(self: "Menu"):
    """display_menu

    display_menu does stuff
    """

    # Clear previous frame render
    self.app.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_DISPLAY

    # Render the Display text
    _ = self.render_button("Display", 10, color=COLOR_RED)

    # Render the fps button
    _ = self.render_button('FPS: ', 8, h_offset=-65)
    text_str = str(self.app.app_config["settings"]["display"]["fps_display"])
    fps_obj = self.render_button(text_str, 8, color=COLOR_PURPLE, h_offset=65)

    # Render the fullscreen button
    _ = self.render_button('Fullscreen: ', 6, h_offset=-125)
    text_str = str(self.app.app_config["settings"]["display"]["fullscreen"])
    fullscreen_obj = self.render_button(text_str, 6, color=COLOR_PURPLE, h_offset=125)

    # Render the resolution button options = ["1280x720", "1366×768", "1920×1080", "2560x1440"]
    text_str = 'Resolution:'
    _ = self.render_button(text_str, 4)

    # Render the 720p resolution choice button
    resolution_obj_0 = self.render_button("1280x720", 3, color=COLOR_PURPLE, h_offset=-300, w_offset=10)

    # Render the 768p resolution choice button
    resolution_obj_1 = self.render_button("1366x768", 3, color=COLOR_PURPLE, h_offset=0, w_offset=10)

    # Render the 1080p resolution choice button
    resolution_obj_2 = self.render_button("1920x1080", 3, color=COLOR_PURPLE, h_offset=300, w_offset=10)

    # Render the 1440p resolution choice button
    resolution_obj_3 = self.render_button("2560x1440", 2, color=COLOR_PURPLE, h_offset=0, w_offset=20)

    # Render the Save button
    save_obj = self.render_button("Save", -8, h_offset=125)

    # Render the Return button
    back_obj = self.render_button("Back", -8, h_offset=-125)

    menu = [
        (fps_obj, self.toggle_fps_display, self.prev_menu),
        (fullscreen_obj, self.toggle_fullscreen, self.prev_menu),
        (resolution_obj_0, self.change_resolution, self.prev_menu, "1280x720"),
        (resolution_obj_1, self.change_resolution, self.prev_menu, "1366x768"),
        (resolution_obj_2, self.change_resolution, self.prev_menu, "1920x1080"),
        (resolution_obj_3, self.change_resolution, self.prev_menu, "2560x1440"),
        (save_obj, self.save_settings, 6),
        (back_obj, self.menu_options[MENU_SETTINGS], 4),
    ]

    return menu
