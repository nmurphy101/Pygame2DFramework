#!/usr/bin/env python3

'''
    Entities
    ~~~~~~~~~~

    All the entities in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame
from .main.main import main_menu
from .pause.pause import pause_menu
from .settings.settings import settings_menu
from .game_over.game_over import game_over
from .display.display import display_menu
from .sound.sound import sound_menu

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
