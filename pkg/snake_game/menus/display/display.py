#!/usr/bin/env python3

"""
    Display Menu
    ~~~~~~~~~~

    Display settings menu


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


def display_menu(self):
    """
    display_menu
    ~~~~~~~~~~

    display_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 4

    # Render the Display text
    _ = self.render_button("Display", 10, (255, 0, 0))

    # Render the fps button
    text_str = 'FPS: ' + str(self.game.app.game_config["settings"]["display"]["fps_display"])
    fps_obj = self.render_button(text_str, 8)

    # Render the fullscreen button
    text_str = 'Fullscreen: ' + str(self.game.app.game_config["settings"]["display"]["fullscreen"])
    fullscreen_obj = self.render_button(text_str, 6)

    # Render the resolution button options = ["1280x720", "1366×768", "1920×1080"]
    text_str = 'Resolution:'
    _ = self.render_button(text_str, 4)

    # Render the 720p resolution choice button
    resolution_obj_0 = self.render_button("1280x720", 3, h_offset=-300)

    # Render the 768p resolution choice button
    resolution_obj_1 = self.render_button("1366x768", 3, h_offset=0)

    # Render the 1080p resolution choice button
    resolution_obj_2 = self.render_button("1920x1080", 3, h_offset=300)

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    menu = [
        (fps_obj, self.toggle_fps_display, self.prev_menu),
        (fullscreen_obj, self.toggle_fullscreen, self.prev_menu),
        (resolution_obj_0, lambda: self.change_resolution("1280x720"), self.prev_menu),
        (resolution_obj_1, lambda: self.change_resolution("1366x768"), self.prev_menu),
        (resolution_obj_2, lambda: self.change_resolution("1920x1080"), self.prev_menu),
        (back_obj, self.settings_menu, 4),
    ]

    return menu
