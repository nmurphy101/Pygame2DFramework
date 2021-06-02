#!/usr/bin/env python3

'''
    Display Menu
    ~~~~~~~~~~

    Display settings menu


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def display_menu(self):
    '''
    display_menu
    ~~~~~~~~~~

    display_menu does stuff
    '''
    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 4

    # Render the Display text
    _ = self.render_button("Display", 10, (255, 0, 0))

    # Render the fps button
    text_str = 'FPS: ' + str(self.game.game_config["settings"]["display"]["fps_display"])
    fps_obj = self.render_button(text_str, 8)

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    menu = [
        (fps_obj, self.toggle_fps_display, self.prev_menu),
        (back_obj, self.SettingsMenu, 4),
    ]

    return menu
