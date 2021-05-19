#!/usr/bin/env python3

'''
    Snake Game
    ~~~~~~~~~~

    Defines the game of snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import os
import gc
# import threading
# import logging
from datetime import datetime
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import json
import pygame
# pylint: disable=relative-beyond-top-level
from pygame import (
    freetype
)
# All the game entities
from .entities.entities import (
    Snake, Food, TelePortal,
)
# All the game menus
from .menus.menus import Menu
from .ai.ai import DecisionBox
# pylint: enable=relative-beyond-top-level


class SnakeGame():
    '''
    SnakeGame
    ~~~~~~~~~~

    SnakeGame for the snake
    '''
    def __init__(self, alpha_screen, screen, app):
        # Calling game platform
        self.app = app
        # Game config file
        self.game_config_file_path = os.path.join(os.path.dirname(__file__), 'game_config.json')
        with open(self.game_config_file_path) as json_data_file:
            self.game_config = json.load(json_data_file)
        # Set starting fps from the config file
        self.app.fps = int(self.game_config["settings"]["display"]["fps"])
        # Window settings
        self.title = app.title + "Snake"
        pygame.display.set_caption(self.title)
        self.screen = screen
        self.alpha_screen = alpha_screen
        screen_w, screen_h = screen.get_size()
        self.screen_size = (screen_w, screen_h)
        self.game_font = freetype.Font(
            file='assets/fonts/PressStart2P-Regular.ttf',
            size=32,
        )
        # Game settings
        self.pause_game_music = False
        # Game music
        self.game_music_intro = "assets/music/8bit_Stage1_Intro.wav"
        self.game_music_loop = "assets/music/8bit_Stage1_Loop.wav"
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        pygame.mixer.music.load(self.game_music_intro)
        pygame.mixer.music.set_volume(float(self.game_config["settings"]["sound"]["music_volume"]))
        # Game Sounds
        self.sounds = [
            pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav"),
            pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav"),
            pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/SciFi05.wav"),
        ]
        # Game timer
        self.timer = None
        # Game object containers
        self.obj_container = []
        self.sprite_group = pygame.sprite.Group()
        # AI blackbox
        self.chosen_ai = None
        # Menu Obj
        self.menu = Menu(self)

    def play(self):
        '''
        play
        ~~~~~~~~~~

        play does stuff
        '''

        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Check if not in a menu
        if self.menu.menu_option is None:
            # Execute game object actions
            for obj in self.obj_container:
                # try to spawn if obj can
                obj.spawn(self.obj_container)
                # Draw game objects
                obj.draw(self.screen, self.obj_container)
                # try to choose a direction if obj can
                obj.choose_direction()
                # Try to move if obj can
                obj.move()
                # collision of obj to other objects/children-of-other-objs
                obj.collision_checks()
            # The game loop FPS counter
            self.app.update_fps()

        else:
            # The game loop FPS counter
            self.app.update_fps()
            # Show which ever menu option that has been chosen
            return self.menu.menu_options.get(self.menu.menu_option)()

    def start(self):
        '''
        start
        ~~~~~~~~~~

        start does stuff
        '''
        # Check settings
        self.settings_checks()
        # Starting variables
        self.menu.menu_option = None
        self.pause_game_music = False
        # AI blackbox
        self.chosen_ai = DecisionBox()
        # Initilize game objects
        food = Food(self.alpha_screen, self.screen, self.screen_size, self.app)
        food2 = Food(self.alpha_screen, self.screen, self.screen_size, self.app)
        # player_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app, player=True)
        # player_snake.movement = 1
        enemy_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
        enemy_snake.movement = 1
        enemy_snake2 = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
        enemy_snake2.movement = 1
        tele_portal = TelePortal(self.alpha_screen, self.screen, self.screen_size, self.app)
        # Set of game objects
        self.obj_container = [ # Order of these objects actually matter
            food,
            food2,
            tele_portal,
            # player_snake,
            enemy_snake,
            enemy_snake2,
        ]
        # Sprite Group obj
        for obj in self.obj_container:
            self.sprite_group.add(obj)
        # Start the game timer
        self.timer = datetime.now()

    def clean_up(self):
        '''
        clean_up
        ~~~~~~~~~~

        clean_up does stuff
        '''
        # Game settings
        self.pause_game_music = False
        # Game timer
        self.timer = None
        # Game object list
        self.obj_container = []
        # AI blackbox
        self.chosen_ai = None
        # Menu Obj
        self.menu = Menu(self)
        # Free unreferenced memory
        gc.collect()

    def settings_checks(self):
        '''
        settings_checks
        ~~~~~~~~~~

        settings_checks does stuff
        '''
        # Start the game music
        if self.game_config["settings"]["sound"]["music"]:
            self.current_track = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.set_volume(float(self.game_config["settings"]["sound"]["music_volume"]))
            pygame.mixer.music.play(0, 0, 1)
        else:
            pygame.mixer.music.pause()

    def quit_game(self):
        '''
        quit_game
        ~~~~~~~~~~

        quit_game does stuff
        '''
        self.app.running = False

    def unpause(self):
        '''
        unpause
        ~~~~~~~~~~

        unpause does stuff
        '''
        self.menu.menu_option = None
        self.pause_game_music = True


def psudo_func(test):
    '''
    psudo_func
    ~~~~~~~~~~

    psudo_func does stuff
    '''
    print("Psudo_func: ", test)
