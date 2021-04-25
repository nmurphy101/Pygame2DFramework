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
# import threading
# import logging
# import sys
# import time
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import json
import random
import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)
# pylint: enable=no-name-in-module


class Snake():
    '''
    Snake
    ~~~~~~~~~~

    AI for the snake
    '''
    def __init__(self, screen, base_game):
        # Window to draw to
        self.screen = screen
        # Snake is dead or alive
        self.alive = True
        # Where the snake was located
        self.prev_pos_x = 96
        self.prev_pos_y = 96
        # Where the snake is located
        self.pos_x = 96
        self.pos_y = 112
        # How big snake parts are
        self.size = 16
        # How fast the snake can move per loop-tick
        self.speed = 1.5
        self.moved_last_cnt = 0
        # Where snake was looking = (North = 0, East = 1, South = 2, West = 3)
        self.prev_direction = 2
        # Where snake is looking = (North = 0, East = 1, South = 2, West = 3)
        self.direction = 2
        # Determines how far the snake can see ahead of itself in the direction it's looking
        self.sight = 5
        # head pos/size  = (left, top, width, height)
        self.head = (self.pos_x, self.pos_y, self.size+8, self.size)
        # head color = red
        self.head_color = (255, 0, 0)
        # Snake is a rectangle object
        self.rect = pygame.draw.rect(self.screen, self.head_color, self.head)
        # Snake death sound
        self.sound_death = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav")
        self.sound_death.set_volume(base_game.effect_volume/3.5)
        # Number of tail segments
        self.num_tails = 5
        # tail segment list
        self.children = []
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(self.screen, self, pos))
            else:
                self.children.append(TailSegment(self.screen, self.children[pos-1], pos))

    def draw(self):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:

            # Draw each tail
            for tail in self.children:
                tail.draw()

             # head pos/size  = (left, top, width, height)
            self.head = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the snake's head based on it's parameters
            self.rect = pygame.draw.rect(self.screen, self.head_color, self.head)

    def grow(self, food):
        '''
        grow
        ~~~~~~~~~~

        grow does stuff
        '''
        # Add a new tail segment
        for _ in range(food.growth):
            self.children.append(TailSegment(
                self.screen,
                self.children[self.num_tails - 1],
                self.num_tails + 1
            ))
            self.num_tails += 1

    def choose_direction(self):
        '''
        choose_direction
        ~~~~~~~~~~

        choose_direction does stuff
        '''
        key = pygame.key.get_pressed()

        if key[K_UP] and self.direction != 0 and self.prev_direction != 2:
            self.direction = 0
        elif key[K_DOWN] and self.direction != 2 and self.prev_direction != 0:
            self.direction = 2
        elif key[K_LEFT] and self.direction != 3 and self.prev_direction != 1:
            self.direction = 3
        elif key[K_RIGHT] and self.direction != 1 and self.prev_direction != 3:
            self.direction = 1

    def move(self):
        '''
        move
        ~~~~~~~~~~

        move does stuff
        '''
        if self.moved_last_cnt > self.speed:
            # Save current position as last position
            self.prev_pos_x = self.pos_x
            self.prev_pos_y = self.pos_y
            # Moving up
            if self.direction == 0:
                self.prev_direction = self.direction
                self.pos_y -= self.size
            # Moving down
            elif self.direction == 2:
                self.prev_direction = self.direction
                self.pos_y += self.size
            # Moving left
            elif self.direction == 3:
                self.prev_direction = self.direction
                self.pos_x -= self.size
            # Moving right
            elif self.direction == 1:
                self.prev_direction = self.direction
                self.pos_x += self.size
            self.moved_last_cnt = 0
        else:
            self.moved_last_cnt += 1


class TailSegment():
    '''
    TailSegment
    ~~~~~~~~~~

    Tail Segment for the snake
    '''
    def __init__(self, screen, ahead_obj, position):
        # Window to draw to
        self.screen = screen
        # Tail is dead or alive
        self.alive = True
        # obj ahead of this obj in the chain of tails/head
        self.ahead_obj = ahead_obj
        # position in the chain of tails/head
        self.position = position
        # How big tail parts are
        self.size = 16
        # Where the tail was/is located
        self.prev_pos_x = ahead_obj.pos_x # was
        self.pos_x = ahead_obj.prev_pos_x # is
        if position == 0:
            self.prev_pos_y = ahead_obj.pos_y-self.size # was
            self.pos_y = ahead_obj.prev_pos_y-self.size # is
        else:
            self.prev_pos_y = ahead_obj.prev_pos_y # was
            self.pos_y = ahead_obj.prev_pos_y # is
        # tail pos/size = (left, top, width, height)
        self.tail = (self.pos_x, self.pos_y, self.size+8, self.size)
        # tail color = white
        self.tail_color = (255, 255, 255)
        # Tail is a rectangle object
        self.rect = pygame.draw.rect(self.screen, self.tail_color, self.tail)

    def draw(self):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Save current position as last position
            self.prev_pos_x = self.pos_x
            self.prev_pos_y = self.pos_y
            # Where the tail is located
            self.pos_x = self.ahead_obj.prev_pos_x
            self.pos_y = self.ahead_obj.prev_pos_y
            # Set the current tail position and size
            self.tail = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the tail segment based on it's parameters
            self.rect = pygame.draw.rect(self.screen, self.tail_color, self.tail)


class Food():
    '''
    Food
    ~~~~~~~~~~

    Food for the snake
    '''
    def __init__(self, screen, screen_size, base_game):
        # Window to draw to
        self.screen = screen
        # Food is dead or alive
        self.alive = False
        # Size of the game screen
        self.screen_size = screen_size
        # Where the food is located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        # How big food parts are
        self.size = 16
        # food pos/size = (left, top, width, height)
        self.food = (self.pos_x, self.pos_y, self.size, self.size)
        # food color = green
        self.food_color = (0, 255, 0)
        # Food is rect obj
        self.rect = pygame.draw.rect(self.screen, self.food_color, self.food)
        # How much a snake grows from eating food
        self.growth = 5
        # Point value of the food
        self.point_value = 10
        # Interact sound
        self.sound_interact = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav")
        self.sound_interact.set_volume(base_game.effect_volume)

    def draw(self):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # food pos/size = (left, top, width, height)
            self.food = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the food segment based on it's parameters
            self.rect = pygame.draw.rect(self.screen, self.food_color, self.food)

    def spawn(self, obj_dict):
        '''
        spawn
        ~~~~~~~~~~

        spawn does stuff
        '''
        # take the game obj_dict
        # First check the locations of all other objects first
        # then pick a random location that isn't taken alrady

        found_spawn = False
        while not found_spawn:
            # Where the food is located
            self.pos_x = self.screen_size[0] - random.randrange(
                16, self.screen_size[0], 16
            )
            self.pos_y = self.screen_size[1] - random.randrange(
                16, self.screen_size[1], 16
            )
            # Check if the chosen random spawn location is taken
            print(obj_dict["food"])
            collision_objs = obj_dict["food"].rect.collidedictall(obj_dict, 1)
            if len(collision_objs) < 1:
                continue
            print("COLLISION 1: ", len(collision_objs))
            for _, obj in obj_dict.items():
                try:
                    if obj.children:
                        collision_obj = obj_dict["food"].rect.collidelist(obj.children)
                        print("COLLISION 2: ", collision_obj)
                except AttributeError:
                    pass
            found_spawn = True

        self.alive = True


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
        print(self.game_config_file_path)
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
        self.score = 0
        self.pause_game_music = False
        self.menu_option = 0
        self.prev_menu = 0
        self.game_menus = [self.main_menu, self.pause_menu, 
                           self.settings_menu, self.game_over_menu,]
        # Game music
        self.game_music_file = "assets/music/Cheerful_Piano_NES.wav"
        pygame.mixer.music.load(self.game_music_file)
        pygame.mixer.music.set_volume(base_game.music_volume)
        
        # Game object list
        self.obj_dict = {}

    def play(self):
        '''
        play
        ~~~~~~~~~~

        play does stuff
        '''

        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Check if in a menu
        if self.menu_option is None:
            self.check_settings()

            # Spawn a new food after it's eaten
            if not self.obj_dict["food"].alive:
                self.obj_dict["food"].spawn(self.obj_dict)

            ## Draw game Objects
            self.obj_dict["food"].draw()
            self.obj_dict["snake"].draw()
            pygame.display.update()

            ## Game logic
            # Snake control and movement
            self.obj_dict["snake"].choose_direction()
            self.obj_dict["snake"].move()
            # collision of objects
            self.collision_checks()
        else:
            if self.menu_option == 0:
                # show the game main menu
                return self.main_menu(self.prev_menu)
            elif self.menu_option == 1:
                # show the pause menu
                return self.pause_menu(self.prev_menu)
            elif self.menu_option == 2:
                # show the pause menu
                return self.settings_menu(self.prev_menu)
            elif self.menu_option == 3:
                # show the pause menu
                return self.game_over_menu(self.prev_menu)

    def start(self, prev_menu):
        '''
        start
        ~~~~~~~~~~

        start does stuff
        '''
        # Start the game music
        if self.game_config["settings"]["music"]:
            pygame.mixer.music.play(-1)
        # Starting variables
        self.score = 0
        self.menu_option = None
        self.pause_game_music = False
        # Initilize game objects
        food = Food(self.screen, self.screen_size, self.base_game)
        snake = Snake(self.screen, self.base_game)
        self.obj_dict = {
            "snake": snake,
            "food": food,
        }

    def collision_checks(self):
        '''
        collision_checks
        ~~~~~~~~~~

        collision_checks does stuff
        '''
        # Collision check between snake and food
        if self.obj_dict["snake"].rect.colliderect(self.obj_dict["food"]):
            pygame.mixer.Sound.play(self.obj_dict["food"].sound_interact)
            self.obj_dict["food"].alive = False
            self.obj_dict["snake"].grow(self.obj_dict["food"])
            self.up_score(self.obj_dict["food"].point_value)
        # Collision check for edge of screen
        if (self.obj_dict["snake"].pos_x > self.screen_size[0]-self.obj_dict["snake"].size) or (
                self.obj_dict["snake"].pos_y > self.screen_size[1]-self.obj_dict["snake"].size):
            pygame.mixer.Sound.play(self.obj_dict["snake"].sound_death)
            self.menu_option = 3
        elif self.obj_dict["snake"].pos_x < 0 or self.obj_dict["snake"].pos_y < 0:
            pygame.mixer.Sound.play(self.obj_dict["snake"].sound_death)
            self.menu_option = 3
        # Collision check between snake and tails
        i = 0
        for tail in self.obj_dict["snake"].children:
            # Skip the first tail segment
            if i > 0:
                if self.obj_dict["snake"].rect.colliderect(tail):
                    pygame.mixer.Sound.play(self.obj_dict["snake"].sound_death)
                    self.menu_option = 3
            i += 1

    def check_settings(self):
        '''
        check_settings
        ~~~~~~~~~~

        check_settings does stuff
        '''
        # Check game music status
        if self.game_config["settings"]["music"]:
            if self.pause_game_music:
                pygame.mixer.music.pause()
            else:
                if self.pause_game_music is None:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.stop()

    def up_score(self, point_value):
        '''
        up_score
        ~~~~~~~~~~

        up_score does stuff
        '''
        # Increase the score
        self.score += point_value
        
    def quit_game(self, prev_menu):
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

    def unpause(self, prev_menu):
        '''
        unpause
        ~~~~~~~~~~

        unpause does stuff
        '''
        self.menu_option = None
        self.pause_game_music = True
    
    def toggle_game_music(self, prev_menu):
        '''
        toggle_game_music
        ~~~~~~~~~~

        toggle_game_music does stuff
        '''
        self.game_config["settings"]["music"] = not self.game_config["settings"]["music"]
        with open(self.game_config_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.game_config, f, ensure_ascii=False, indent=4)

    def main_menu(self, prev_menu):
        '''
        main_menu
        ~~~~~~~~~~

        main_menu does stuff
        '''
        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Make sure the right menu option is selected
        self.menu_option = 0

        # Check settings if just left settings page
        if prev_menu == 2:
            self.check_settings()

        # Render the Main Menu text
        text_str = 'Main Menu'
        _ = self.game_font.render_to(
            self.screen,
            (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
             self.screen_size[1]/2 - self.game_font.size*8),
            text_str,
            (255, 0, 0)
        )

        # Render the play button
        text_str = 'Play'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size)
        play_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the settings button
        text_str = 'Settings'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size)
        settings_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the quit button
        text_str = 'Quit'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size*3)
        quit_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Update the screen display
        pygame.display.update()

        menu = [
            (play_obj, self.start, 0),
            (settings_obj, self.settings_menu, 0),
            (quit_obj, self.quit_game, 0),
        ]

        return menu

    def pause_menu(self, prev_menu):
        '''
        pause_menu
        ~~~~~~~~~~

        pause_menu does stuff
        '''

        # Make sure the right menu option is selected
        self.menu_option = 1

        # Check settings if just left settings page
        if prev_menu == 2:
            self.check_settings()

        # Pause game music
        self.pause_game_music = True
        # Render the Game Over text
        text_str = 'Paused'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*8)
        _ = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 0, 0)
        )

        # Render the score
        text_str = 'Score: ' + str(self.score)
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*6)
        _ = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 0, 0)
        )

        # Render the quit button
        text_str = 'Resume'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*1)
        resume_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the settings button
        text_str = 'Settings'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size)
        settings_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the quit button
        text_str = 'Quit'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size*3)
        return_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Update the screen display
        pygame.display.update()

        menu = [
            (resume_obj, self.unpause, 1),
            (settings_obj, self.settings_menu, 1),
            (return_obj, self.main_menu, 1),
        ]

        return menu

    def settings_menu(self, prev_menu):
        '''
        settings_menu
        ~~~~~~~~~~

        settings_menu does stuff
        '''
        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Make sure the right menu option is selected
        self.menu_option = 2

        # Render the Settings Menu text
        text_str = 'Settings Menu'
        _ = self.game_font.render_to(
            self.screen,
            (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
             self.screen_size[1]/2 - self.game_font.size*8),
            text_str,
            (255, 0, 0)
        )

        # Render the play button
        text_str = 'Music: ' + str(self.game_config["settings"]["music"])
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*2)
        music_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the Return button
        text_str = 'Return'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size*6)
        return_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Update the screen display
        pygame.display.update()

        menu = [
            (music_obj, self.toggle_game_music, prev_menu),
            # (settings_obj, psudo_func),
            (return_obj, self.game_menus[prev_menu], 2),
        ]

        return menu

    def game_over_menu(self, prev_menu):
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
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*8)
        _ = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 0, 0)
        )
        # Render the score
        text_str = 'Score: ' + str(self.score)
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 - self.game_font.size*6)
        _ = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 0, 0)
        )

        # Render the restart button
        text_str = 'Restart'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size)
        restart_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Render the quit button
        text_str = 'Quit'
        position = (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
                    self.screen_size[1]/2 + self.game_font.size*3)
        return_obj = self.game_font.render_to(
            self.screen,
            position,
            text_str,
            (255, 255, 255)
        )

        # Update the screen display
        pygame.display.update()

        menu = [
            (restart_obj, self.start, 3),
            (return_obj, self.main_menu, 3),
        ]

        return menu


def psudo_func():
    pass
