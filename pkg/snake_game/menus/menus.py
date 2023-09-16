#!/usr/bin/env python3

'''
    Entities
    ~~~~~~~~~~

    All the entities in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import json
import pygame
from pygame import (
    DOUBLEBUF, FULLSCREEN
)

from .home import home_menu
from .pause import pause_menu
from .settings import settings_menu
from .game_over import game_over
from .display import display_menu
from .sound import sound_menu


class Menu():
    '''
    Menu
    ~~~~~~~~~~

    All menus for the game
    '''

    def __init__(self, game):
        """AI is creating summary for __init__

        Args:
            game ([type]): [description]
        """

        # Game that's calling the menus
        self.game = game

        # Game settings
        self.pause_game_music = self.game.pause_game_music
        self.menu_option = 0
        self.prev_menu = 0
        self.root_menu = 0
        self.game_menus = [self.home_menu, self.pause_menu,
                           self.settings_menu, self.game_over_menu,
                           self.display_menu, self.sound_menu,]

        # Menu options
        self.menu_options = {
            0: lambda: self.home_menu(),
            1: lambda: self.pause_menu(),
            2: lambda: self.settings_menu(),
            3: lambda: self.game_over_menu(),
            4: lambda: self.display_menu(),
            5: lambda: self.sound_menu(),
        }


    def home_menu(self):
        """AI is creating summary for home_menu

        Returns:
            [type]: [description]
        """

        return home_menu(self)


    def pause_menu(self):
        """AI is creating summary for pause_menu

        Returns:
            [type]: [description]
        """

        return pause_menu(self)


    def settings_menu(self):
        """AI is creating summary for settings_menu

        Returns:
            [type]: [description]
        """

        return settings_menu(self)


    def game_over_menu(self):
        """AI is creating summary for game_over_menu

        Returns:
            [type]: [description]
        """

        return game_over(self)


    def display_menu(self):
        """AI is creating summary for display_menu

        Returns:
            [type]: [description]
        """

        return display_menu(self)


    def sound_menu(self):
        """AI is creating summary for sound_menu

        Returns:
            [type]: [description]
        """

        return sound_menu(self)


    def render_button(self, title, position, color=(255, 255, 255), h_offset=0, screen=None):
        """AI is creating summary for render_button

        Args:
            title ([type]): [description]
            position ([type]): [description]
            color (tuple, optional): [description]. Defaults to (255, 255, 255).
            h_offset (int, optional): [description]. Defaults to 0.
            screen ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """

        if screen:
            chosen_screen = screen

        else:
            chosen_screen = self.game.screen

        # Render the Display text
        text_str = str(title)

        position = (
            self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2 + h_offset,
            self.game.screen_size[1]/2 - self.game.game_font.size * position
        )

        obj = self.game.game_font.render_to(
            chosen_screen,
            position,
            text_str,
            color
        )

        return obj


    def save_settings(self):
        """AI is creating summary for save_settings
        """

        with open(self.game.app.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.app.game_config, _file, ensure_ascii=False, indent=4)


    def toggle_game_music(self):
        '''
        toggle_game_music
        ~~~~~~~~~~

        toggle_game_music does stuff
        '''

        music = self.game.app.game_config["settings"]["sound"]["music"]
        music = not music
        self.save_settings()


    def increase_music_volume(self):
        '''
        increase_music_volume
        ~~~~~~~~~~

        increase_music_volume does stuff
        '''

        music_volume = self.game.app.game_config["settings"]["sound"]["music_volume"]
        music_volume = str(float(music_volume) + .05)
        self.save_settings()
        pygame.mixer.music.set_volume(float(music_volume))


    def decrease_music_volume(self):
        '''
        decrease_music_volume
        ~~~~~~~~~~

        decrease_music_volume does stuff
        '''

        music_volume = self.game.app.game_config["settings"]["sound"]["music_volume"]
        music_volume = str(float(music_volume) - .05)
        self.save_settings()
        pygame.mixer.music.set_volume(float(music_volume))


    def increase_effect_volume(self):
        '''
        increase_effect_volume
        ~~~~~~~~~~

        increase_effect_volume does stuff
        '''

        self.game.app.game_config["settings"]["sound"]["effect_volume"] = (
            str(float(self.game.app.game_config["settings"]["sound"]["effect_volume"]) + .05)
        )
        self.save_settings()


    def decrease_effect_volume(self):
        '''
        decrease_effect_volume
        ~~~~~~~~~~

        decrease_effect_volume does stuff
        '''

        self.game.app.game_config["settings"]["sound"]["effect_volume"] = (
            str(float(self.game.app.game_config["settings"]["sound"]["effect_volume"]) - .05)
        )
        self.save_settings()


    def increase_menu_volume(self):
        '''
        increase_menu_volume
        ~~~~~~~~~~

        increase_menu_volume does stuff
        '''

        menu_volume = self.game.app.game_config["settings"]["sound"]["menu_volume"]
        menu_volume = (
            str(float(menu_volume) + .05)
        )
        self.save_settings()


    def decrease_menu_volume(self):
        '''
        decrease_menu_volume
        ~~~~~~~~~~

        decrease_menu_volume does stuff
        '''

        menu_volume = self.game.app.game_config["settings"]["sound"]["menu_volume"]
        menu_volume = (
            str(float(menu_volume) - .05)
        )
        self.save_settings()


    def toggle_fps_display(self):
        '''
        toggle_fps_display
        ~~~~~~~~~~

        toggle_fps_display does stuff
        '''

        fps_display = self.game.app.game_config["settings"]["display"]["fps_display"]
        fps_display = not fps_display
        self.save_settings()


    def toggle_fullscreen(self):
        '''
        toggle_fullscreen
        ~~~~~~~~~~

        toggle_fullscreen does stuff
        '''

        full_screen = self.game.app.game_config["settings"]["display"]["fullscreen"]
        full_screen = not full_screen
        self.save_settings()
        pygame.display.toggle_fullscreen()


    def change_resolution(self, resolution):
        '''
        change_resolution
        ~~~~~~~~~~

        change_resolution does stuff
        '''

        self.game.app.game_config["settings"]["display"]["resolution"] = resolution
        self.save_settings()
        self.game.app.screen_width = int(resolution.split("x")[0])
        self.game.app.screen_height = int(resolution.split("x")[1])
        self.game.screen_size = (self.game.app.screen_width, self.game.app.screen_height)

        if self.game.app.game_config["settings"]["display"]["fullscreen"]:
            flags = DOUBLEBUF | FULLSCREEN
        else:
            flags = DOUBLEBUF

        # Modify all game screens with new resolution    (#, RESIZABLE))
        self.game.screen = pygame.display.set_mode(
            (self.game.app.screen_width, self.game.app.screen_height),
            flags,
            16,
        )

        self.game.screen.set_alpha(None)

        self.game.app.debug_screen = pygame.Surface(
            (self.game.app.screen_width, self.game.app.screen_height)
        )

        self.game.app.debug_screen.set_colorkey((0, 0, 0))

        self.game.app.background_0 = pygame.Surface(
            (self.game.app.screen_width, self.game.app.screen_height)
        )

        self.game.app.background_0.set_colorkey((0, 0, 0))
