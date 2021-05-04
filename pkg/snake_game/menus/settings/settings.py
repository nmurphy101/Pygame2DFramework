#!/usr/bin/env python3

'''
    Settings Menu
    ~~~~~~~~~~

    The settings menu with options for different settings menus


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def settings_menu(self):
    '''
    settings_menu
    ~~~~~~~~~~
    settings_menu does stuff
    '''
    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 2

    # Check settings if just left settings page
    if self.prev_menu != 1 and self.prev_menu != 2:
        self.game.settings_checks()

    # Render the Settings Menu text
    text_str = 'Settings'
    _ = self.game.game_font.render_to(
        self.game.screen,
        (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
         self.game.screen_size[1]/2 - self.game.game_font.size*10),
        text_str,
        (255, 0, 0)
    )

    # Render the display button
    text_str = 'Display'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 - self.game.game_font.size
    )
    display_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the Sound button
    text_str = 'Sound'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 + self.game.game_font.size
    )
    sound_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the Return button
    text_str = 'Back'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 + self.game.game_font.size*8
    )
    back_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Update the screen display
    pygame.display.update()

    menu = [
        (display_obj, self.DisplayMenu, 2),
        (sound_obj, self.SoundMenu, 2),
        (back_obj, self.game_menus[self.root_menu], 2),
    ]

    self.prev_menu = 2

    return menu
