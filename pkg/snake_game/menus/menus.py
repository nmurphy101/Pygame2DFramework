#!/usr/bin/env python3

'''
    Entities
    ~~~~~~~~~~

    All the entities in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


class Menu():
    '''
    Menu
    ~~~~~~~~~~

    All menus for the game
    '''
    def __init__(self, game):
        # Game that's calling the menus
        self.game = game
        # Game settings
        self.pause_game_music = self.game.pause_game_music
        self.menu_option = 0
        self.prev_menu = 0
        self.root_menu = 0
        self.game_menus = [self.main_menu, self.pause_menu,
                           self.settings_menu, self.game_over_menu,
                           self.display_menu, self.sound_menu,]

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
        if self.prev_menu == 2:
            self.game.check_settings()

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
            (settings_obj, self.settings_menu, 0),
            (quit_obj, self.game.quit_game, 0),
        ]

        self.prev_menu = 0

        return menu

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
        for name, obj in self.game.obj_dict.items():
            if obj.player:
                score = obj.score
        # Render the score
        text_str = 'Score: ' + str(score)
        position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                    self.game.screen_size[1]/2 - self.game.game_font.size*8)
        _ = self.game.game_font.render_to(
            self.game.screen,
            position,
            text_str,
            (255, 0, 0)
        )

        # Render the quit button
        text_str = 'Resume'
        position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                    self.game.screen_size[1]/2 - self.game.game_font.size)
        resume_obj = self.game.game_font.render_to(
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
            (settings_obj, self.settings_menu, 1),
            (return_obj, self.main_menu, 1),
        ]

        self.prev_menu = 1

        return menu

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
        print("CHECK: ", self.prev_menu)
        if self.prev_menu != 1 and self.prev_menu != 2:
            self.game.check_settings()

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
        position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                    self.game.screen_size[1]/2 - self.game.game_font.size)
        display_obj = self.game.game_font.render_to(
            self.game.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the Sound button
        text_str = 'Sound'
        position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                    self.game.screen_size[1]/2 + self.game.game_font.size)
        sound_obj = self.game.game_font.render_to(
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
            (display_obj, self.display_menu, 2),
            (sound_obj, self.sound_menu, 2),
            (back_obj, self.game_menus[self.root_menu], 2),
        ]

        self.prev_menu = 2

        return menu

    def game_over_menu(self):
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
        for name, obj in self.game.obj_dict.items():
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
            (return_obj, self.main_menu, 3),
        ]

        self.prev_menu = 3

        return menu

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
        position = (self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2,
                    self.game.screen_size[1]/2 - self.game.game_font.size*10)
        _ = self.game.game_font.render_to(
            self.game.screen,
            position,
            text_str,
            (255, 0, 0)
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
            (back_obj, self.settings_menu, 4),
        ]

        self.prev_menu = 4

        return menu

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
            (back_obj, self.settings_menu, 5),
        ]

        self.prev_menu = 5

        return menu
