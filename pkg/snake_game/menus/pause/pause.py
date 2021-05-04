#!/usr/bin/env python3

'''
    Pause Menu
    ~~~~~~~~~~

    Pause menu shown when the game is paused


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def pause_menu(self):
    '''
    pause_menu
    ~~~~~~~~~~

    pause_menu does stuff
    '''

    # Make sure the right menu option is selected
    self.menu_option = 1
    self.root_menu = 1

    # Pause game music
    self.game.pause_game_music = True

    # Render the Game Over text
    text_str = '-Paused-'
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

    # Get the player score
    score = "NA"
    for _, obj in self.game.obj_dict.items():
        if obj.player:
            score = obj.score
    # Render the score
    text_str = 'Score: ' + str(score)
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 - self.game.game_font.size*8
    )
    _ = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 0, 0)
    )

    # Render the quit button
    text_str = 'Resume'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 - self.game.game_font.size
    )
    resume_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the settings button
    text_str = 'Settings'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 + self.game.game_font.size
    )
    settings_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the quit button
    text_str = 'Main Menu'
    position = (
        self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
        self.game.screen_size[1]/2 + self.game.game_font.size*3
    )
    return_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Update the screen display
    pygame.display.update()

    menu = [
        (resume_obj, self.game.unpause, 1),
        (settings_obj, self.SettingsMenu, 1),
        (return_obj, self.MainMenu, 1),
    ]

    return menu
