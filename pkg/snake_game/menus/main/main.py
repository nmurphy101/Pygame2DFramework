#!/usr/bin/env python3

'''
    Main Menu
    ~~~~~~~~~~

    Game Main menu


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def main_menu(self):
    '''
    main_menu
    ~~~~~~~~~~

    main_menu does stuff
    '''
    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 0
    self.root_menu = 0

    # Check settings if just left settings page
    if self.prev_menu not in [1, 2]:
        self.game.check_settings()
        # just to prevent a check settings inf. loop
        self.prev_menu = 2

    # Render the Main Menu text
    text_str = 'Main Menu'
    _ = self.game.game_font.render_to(
        self.game.screen,
        (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 - self.game.game_font.size*8),
        text_str,
        (255, 0, 0)
    )

    # Render the play button
    text_str = 'Play'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 - self.game.game_font.size)
    play_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the settings button
    text_str = 'Settings'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 + self.game.game_font.size)
    settings_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the quit button
    text_str = 'Quit'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 + self.game.game_font.size*3)
    quit_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Update the screen display
    pygame.display.update()

    menu = [
        (play_obj, self.game.start, 0),
        (settings_obj, self.SettingsMenu, 0),
        (quit_obj, self.game.quit_game, 0),
    ]

    return menu
