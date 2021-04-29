#!/usr/bin/env python3

'''
    Game Over Menu
    ~~~~~~~~~~

    The menu screen that is shown when the game is over


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame

def game_over(self):
    '''
    game_over_menu
    ~~~~~~~~~~

    game_over_menu does stuff
    '''

    # Make sure the right menu option is selected
    self.menu_option = 3

    # Stop the music
    pygame.mixer.music.stop()

    # Render the Game Over text
    text_str = 'Game Over'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 - self.game.game_font.size*10)
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
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 - self.game.game_font.size*9)
    _ = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 0, 0)
    )

    # Render the restart button
    text_str = 'Restart'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 - self.game.game_font.size)
    restart_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Render the quit button
    text_str = 'Quit'
    position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                self.game.screen_size[1]/2 + self.game.game_font.size*2)
    return_obj = self.game.game_font.render_to(
        self.game.screen,
        position,
        text_str,
        (255, 255, 255)
    )

    # Update the screen display
    pygame.display.update()

    menu = [
        (restart_obj, self.game.start, 3),
        (return_obj, self.MainMenu, 3),
    ]

    return menu
