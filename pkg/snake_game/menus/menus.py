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
# pylint: disable=relative-beyond-top-level
from .main.main import main_menu
from .pause.pause import pause_menu
from .settings.settings import settings_menu
from .game_over.game_over import game_over
from .display.display import display_menu
from .sound.sound import sound_menu
# pylint: enable=relative-beyond-top-level

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
        self.game_menus = [self.MainMenu, self.PauseMenu,
                           self.SettingsMenu, self.GameOverMenu,
                           self.DisplayMenu, self.SoundMenu,]

    def MainMenu(self):
       return main_menu(self)

    def PauseMenu(self):
        return pause_menu(self)

    def SettingsMenu(self):
        return settings_menu(self)

    def GameOverMenu(self):
        return game_over(self)

    def DisplayMenu(self):
        return display_menu(self)

    def SoundMenu(self):
        return sound_menu(self)

    def render_button(self, title, position, color=(255, 255, 255), h_offset=0):
        # Render the Display text
        text_str = str(title)
        position = (
            self.game.screen_size[0]/2-(len(text_str)*self.game.game_font.size)/2 + h_offset,
            self.game.screen_size[1]/2 - self.game.game_font.size * position
        )
        obj = self.game.game_font.render_to(
            self.game.screen,
            position,
            text_str,
            color
        )

        return obj

    def toggle_game_music(self):
        '''
        toggle_game_music
        ~~~~~~~~~~

        toggle_game_music does stuff
        '''
        self.game.game_config["settings"]["music"] = not self.game.game_config["settings"]["music"]
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)

    def increase_music_volume(self):
        '''
        increase_music_volume
        ~~~~~~~~~~

        increase_music_volume does stuff
        '''
        self.game.game_config["settings"]["music_volume"] = str(float(self.game.game_config["settings"]["music_volume"]) + .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)
        pygame.mixer.music.set_volume(float(self.game.game_config["settings"]["music_volume"]))

    def decrease_music_volume(self):
        '''
        decrease_music_volume
        ~~~~~~~~~~

        decrease_music_volume does stuff
        '''
        self.game.game_config["settings"]["music_volume"] = str(float(self.game.game_config["settings"]["music_volume"]) - .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)
        pygame.mixer.music.set_volume(float(self.game.game_config["settings"]["music_volume"]))

    def increase_effect_volume(self):
        '''
        increase_effect_volume
        ~~~~~~~~~~

        increase_effect_volume does stuff
        '''
        self.game.game_config["settings"]["effect_volume"] = str(float(self.game.game_config["settings"]["effect_volume"]) + .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)

    def decrease_effect_volume(self):
        '''
        decrease_effect_volume
        ~~~~~~~~~~

        decrease_effect_volume does stuff
        '''
        self.game.game_config["settings"]["effect_volume"] = str(float(self.game.game_config["settings"]["effect_volume"]) - .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)

    def increase_menu_volume(self):
        '''
        increase_menu_volume
        ~~~~~~~~~~

        increase_menu_volume does stuff
        '''
        self.game.game_config["settings"]["menu_volume"] = str(float(self.game.game_config["settings"]["menu_volume"]) + .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)

    def decrease_menu_volume(self):
        '''
        decrease_menu_volume
        ~~~~~~~~~~

        decrease_menu_volume does stuff
        '''
        self.game.game_config["settings"]["menu_volume"] = str(float(self.game.game_config["settings"]["menu_volume"]) - .05)
        with open(self.game.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game.game_config, _file, ensure_ascii=False, indent=4)
