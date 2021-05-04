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
    text_str = 'Display'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 - self.game.game_font.size*10
    )
    _ = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 0, 0)
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
        (back_obj, self.SettingsMenu, 4),
    ]

    return menu
