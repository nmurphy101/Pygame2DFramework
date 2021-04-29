#!/usr/bin/env python3

'''
    Sound Menu
    ~~~~~~~~~~

    Sound settings menu


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def sound_menu(self):
    '''
    sound_menu
    ~~~~~~~~~~

    sound_menu does stuff
    '''
    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 5

    # Render the music button
    text_str = 'Music: ' + str(self.game.game_config["settings"]["music"])
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 - self.game.game_font.size)
    music_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the Return button
    text_str = 'Back'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 + self.game.game_font.size*8)
    back_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Update the screen display
    pygame.display.update()

    menu = [
        (music_obj, self.game.toggle_game_music, self.prev_menu),
        (back_obj, self.SettingsMenu, 5),
    ]

    return menu
