#!/usr/bin/env python3

'''
    Snake Ai
    ~~~~~~~~~~

    Its the ai for the snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import os
import sys
import time
# import threading
# import logging
# import sys
# import time
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import json
import pygame
# pylint: disable=relative-beyond-top-level
# All the game entities
from .entities.entities import (
    Snake, Food, TelePortal,
)
# All the game menus
from .menus.menus import Menu
# pylint: enable=relative-beyond-top-level


class SnakeGame():
    '''
    SnakeGame
    ~~~~~~~~~~

    SnakeGame for the snake
    '''
    def __init__(self, screen, game_font, base_game):
        # Calling game platform
        self.base_game = base_game
        # Game config file
        self.game_config_file_path = os.path.join(os.path.dirname(__file__), 'game_config.json')
        with open(self.game_config_file_path) as json_data_file:
            self.game_config = json.load(json_data_file)
        # Window settings
        self.title = base_game.title + "Snake"
        pygame.display.set_caption(self.title)
        self.screen = screen
        self.game_font = game_font
        screen_w, screen_h = screen.get_size()
        self.screen_size = (screen_w, screen_h)
        # Game settings
        self.pause_game_music = False
        # Game music
        self.game_music_intro = "assets/music/8bit_Stage1_Intro.wav"
        self.game_music_loop = "assets/music/8bit_Stage1_Loop.wav"
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        pygame.mixer.music.load(self.game_music_intro)
        pygame.mixer.music.set_volume(base_game.music_volume)
        # Game timer
        # self.timer = time.time()
        # Game object list
        self.obj_dict = {}
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

            # update the display
            pygame.display.update()

            # collision of objects
            self.collision_checks()

        else:
            # show the game main menu
            if self.menu.menu_option == 0:
                return self.menu.MainMenu()
            # show the pause menu
            elif self.menu.menu_option == 1:
                return self.menu.PauseMenu()
            # show the pause menu
            elif self.menu.menu_option == 2:
                return self.menu.SettingsMenu()
            # show the pause menu
            elif self.menu.menu_option == 3:
                return self.menu.GameOverMenu()
            # show the display menu
            elif self.menu.menu_option == 4:
                return self.menu.DisplayMenu()
            # show the display menu
            elif self.menu.menu_option == 5:
                return self.menu.SoundMenu()

    def start(self):
        '''
        start
        ~~~~~~~~~~

        start does stuff
        '''
        # Check settings
        self.check_settings()

        # Starting variables
        self.menu.menu_option = None
        self.pause_game_music = False

        # Initilize game objects
        food = Food(self.screen, self.screen_size, self.base_game)
        snake = Snake(self.screen, self.screen_size, self.base_game)
        tele_portal = TelePortal(self.screen, self.screen_size, self.base_game)
        self.obj_dict = {
            snake.ID: snake,
            food.ID: food,
            tele_portal.ID: tele_portal,
        }

    def collision_checks(self):
        '''
        collision_checks
        ~~~~~~~~~~

        collision_checks does stuff
        '''
        items = self.obj_dict.items()
        # Collision check for all entities
        for _, obj1 in items:
            for _, obj2 in items:
                # Make sure not checking collision with dead obj's
                if obj1.alive and obj2.alive:
                    # Make sure not checking collision with self
                    if obj1 != obj2:
                        # Collision check between obj and other obj
                        if obj1.rect.colliderect(obj2):
                            print(obj2, " Interacting with ", obj1)
                            obj2.interact(obj1)
                        # Collision check for edge of screen (Right and Bottom)
                        if (obj1.pos_x > self.screen_size[0]-obj1.size) or (
                                obj1.pos_y > self.screen_size[1]-obj1.size):
                            if obj1.killable:
                                print("Edge of screen 1")
                                sound = obj1.sound_death
                                sound.set_volume(obj1.sound_death_volume)
                                pygame.mixer.Sound.play(sound)
                                # Loose the game if obj1 is the player
                                if obj1.player:
                                    self.menu.menu_option = 3
                                # Kill obj1
                                obj1.alive = False
                        # Collision check for edge of screen (Left and Top)
                        elif obj1.pos_x < 0 or obj1.pos_y < 0:
                            if obj1.killable:
                                print("Edge of screen 2")
                                sound = obj1.sound_death
                                sound.set_volume(obj1.sound_death_volume)
                                pygame.mixer.Sound.play(sound)
                                # Loose the game if obj1 is the player
                                if obj1.player:
                                    self.menu.menu_option = 3
                                # Kill obj1
                                obj1.alive = False
                    # Collision check between obj1 and obj2's children even if obj1=obj2
                    obj2.interact_children(obj1)

    def check_settings(self):
        '''
        check_settings
        ~~~~~~~~~~

        check_settings does stuff
        '''
        # Start the game music
        if self.game_config["settings"]["music"]:
            self.current_track = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play(0, 0, 1)
        elif not self.game_config["settings"]["music"]:
            pygame.mixer.music.pause()

    def quit_game(self):
        '''
        quit_game
        ~~~~~~~~~~

        quit_game does stuff
        '''
        self.base_game.running = False
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

    def toggle_game_music(self):
        '''
        toggle_game_music
        ~~~~~~~~~~

        toggle_game_music does stuff
        '''
        self.game_config["settings"]["music"] = not self.game_config["settings"]["music"]
        with open(self.game_config_file_path, 'w', encoding='utf-8') as _file:
            json.dump(self.game_config, _file, ensure_ascii=False, indent=4)


def psudo_func(name1, name2):
    pass
