#!/usr/bin/env python3

'''
    Snake Game
    ~~~~~~~~~~

    Defines the game of snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import os
import sys
# import threading
# import logging
# import sys
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
        # Game object list
        self.obj_dict = {}
        # AI blackbox
        self.chosen_ai = DecisionBox()
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
            for _, obj in self.obj_dict.items():
                try:
                    # try to spawn if obj can
                    obj.spawn(self.obj_dict)
                except AttributeError:
                    pass

                # Draw game objects
                obj.draw(self.screen, self.obj_dict)

                try:
                    # try to choose a direction if obj can
                    obj.choose_direction()
                except AttributeError:
                    pass

                try:
                    # Try to move if obj can
                    obj.move()
                except AttributeError:
                    pass

                try:
                    # collision of obj to other objects/children-of-objs
                    self.collision_checks(obj)
                except AttributeError:
                    pass

            # The game loop FPS counter
            self.app.update_fps()

        else:
            # Show which ever menu option that has been chosen
            return self.menu.menu_options.get(self.menu.menu_option)()

    def start(self):
        '''
        start
        ~~~~~~~~~~

        start does stuff
        '''
        # Clear game objects up to free memory
        self.clean_up()
        # Start the game timer
        self.timer = datetime.now()
        # Check settings
        self.settings_checks()
        # Starting variables
        self.menu.menu_option = None
        self.pause_game_music = False
        # Initilize game objects
        food = Food(self.alpha_screen, self.screen, self.screen_size, self.app)
        food2 = Food(self.alpha_screen, self.screen, self.screen_size, self.app)
        # player_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app, player=True)
        # player_snake.speed = .75
        enemy_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
        enemy_snake.speed = 1
        enemy_snake2 = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
        enemy_snake2.speed = 1
        tele_portal = TelePortal(self.alpha_screen, self.screen, self.screen_size, self.app)
        self.obj_dict = { # Order of these objects actually matter
            food.ID: food,
            food2.ID: food2,
            tele_portal.ID: tele_portal,
            # player_snake.ID: player_snake,
            enemy_snake.ID: enemy_snake,
            enemy_snake2.ID: enemy_snake2,
        }

    def clean_up(self):
        '''
        clean_up
        ~~~~~~~~~~

        clean_up does stuff
        '''
        # Game object list
        self.obj_dict = {}
        # AI blackbox
        self.chosen_ai = DecisionBox()
        # Menu Obj
        self.menu = Menu(self)

    def collision_checks(self, obj1):
        '''
        collision_checks
        ~~~~~~~~~~

        collision_checks does stuff
        '''
        items = self.obj_dict.items()
        # Collision check for all entities
        for _, obj2 in items:
            # Make sure not checking collision with dead obj's
            if obj1.alive and obj2.alive:
                # Make sure not checking collision with self
                if obj1 != obj2:
                    # Collision check between obj and other obj
                    self.check_obj_to_obj_collision(obj1, obj2)
                    # Screen edge collision check
                    self.check_edge_collision(obj1)
                # Collision check between obj1 and obj2's children even if obj1=obj2
                obj2.interact_children(obj1)

    def check_edge_collision(self, obj1):
        '''
        check_edge_collision
        ~~~~~~~~~~

        Check for obj1 collision/interaction to the edge of the screen
        '''
        # Collision check for edge of screen (Right and Bottom)
        if (obj1.pos_x > self.screen_size[0]-obj1.size) or (
                obj1.pos_y > self.screen_size[1]-obj1.size):
            obj1.die("Edge of screen")
        # Collision check for edge of screen (Left and Top)
        elif obj1.pos_x < 0 or obj1.pos_y < 0:
            obj1.die("Edge of screen")

    def check_obj_to_obj_collision(self, obj1, obj2):
        '''
        check_obj_to_obj_collision
        ~~~~~~~~~~

        Check for obj1 to obj2 collision/interaction
        '''
        # Collision check between obj1 and other obj2
        if obj1.rect.colliderect(obj2):
            if obj1.secondary_target:
                obj1.secondary_target = None

            # print(obj1, " Interacting with ", obj2)
            # Do obj2's interaction method
            obj2.interact(obj1)

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
        #pylint: disable=no-member
        pygame.display.quit()
        pygame.quit()
        #pylint: enable=no-member
        sys.exit()

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
