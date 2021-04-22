#!/usr/bin/env python3

'''
    Snake Ai
    ~~~~~~~~~~

    Its the ai for the snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


# import os
# import threading
# import logging
# import sys
# import time
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import random
import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_ESCAPE,
    ACTIVEEVENT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST,
)
# pylint: enable=no-name-in-module


class Snake():
    '''
    Snake
    ~~~~~~~~~~

    AI for the snake
    '''
    def __init__(self, screen):
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
        self.prev_direction = -1
        # Where snake is looking = (North = 0, East = 1, South = 2, West = 3)
        self.direction = 1
        # Determines how far the snake can see ahead of itself in the direction it's looking
        self.sight = 5
        # head pos/size  = (left, top, width, height)
        self.head = (self.pos_x, self.pos_y, self.size+8, self.size)
        # head color = red
        self.head_color = (255, 0, 0)
        # Snake is a rectangle object
        self.rect = pygame.draw.rect(self.screen, self.head_color, self.head)
        # Number of tail segments
        self.num_tails = 5
        # tail segment list
        self.tail_segments = []
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.tail_segments.append(TailSegment(self.screen, self, pos))
            else:
                self.tail_segments.append(TailSegment(self.screen, self.tail_segments[pos-1], pos))

    def draw(self):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:

            # Draw each tail
            for tail in self.tail_segments:
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
            self.tail_segments.append(TailSegment(
                self.screen,
                self.tail_segments[self.num_tails - 1],
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
    def __init__(self, screen, screen_size):
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
        self.rect = None
        # food color = green
        self.food_color = (0, 255, 0)
        # How much a snake grows from eating food
        self.growth = 5
        # Point value of the food
        self.point_value = 10

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

    def spawn(self):
        '''
        spawn
        ~~~~~~~~~~

        spawn does stuff
        '''
        # Where the food is located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )

        self.alive = True


class SnakeGame():
    '''
    SnakeGame
    ~~~~~~~~~~

    SnakeGame for the snake
    '''
    def __init__(self, screen, game_font):
        self.screen = screen
        self.game_font = game_font
        screen_w, screen_h = screen.get_size()
        self.screen_size = (screen_w, screen_h)
        self.score = 0
        self.game_over = False
        self.running = True
        self.pause = False
        self.focus_pause = False
        self.obj_dict = {}

    def play(self):
        '''
        play
        ~~~~~~~~~~

        play does stuff
        '''

        clock = pygame.time.Clock()

        # Initilize game objects
        self.start()

        # Game loop
        while self.running:
            # System/window events to be checked
            self.event_checks()

            # Check if the game is over
            if not self.game_over:
                # Check if the game is paused
                if not self.pause and not self.focus_pause:
                    # Clear previous frame render
                    self.screen.fill((0, 0, 0, 0))

                    # Spawn a new food after it's eaten
                    if not self.obj_dict["food"].alive:
                        self.obj_dict["food"].spawn()

                    ## Draw game Objects
                    self.obj_dict["food"].draw()
                    self.obj_dict["snake"].draw()
                    pygame.display.update()

                    ## Game logic
                    # Snake control and movement
                    self.obj_dict["snake"].choose_direction()
                    self.obj_dict["snake"].move()
                    # collision of objects
                    self.collision_checks(self.screen_size)

                else:
                    # show the pause menu
                    self.pause_menu()
            else:
                # show the game over menu
                self.game_over_menu()

            # The game loop FPS
            clock.tick(60)

        # pylint: disable=no-member
        pygame.quit()
        # pylint: enable=no-member

    def start(self):
        '''
        start
        ~~~~~~~~~~

        start does stuff
        '''
        # Set the score to 0
        self.score = 0
        self.pause = False
        self.focus_pause = False
        # Initilize game objects
        food = Food(self.screen, self.screen_size)
        snake = Snake(self.screen)
        self.obj_dict = {
            "snake": snake,
            "food": food,
        }

    def up_score(self, point_value):
        '''
        up_score
        ~~~~~~~~~~

        up_score does stuff
        '''
        # Increase the score
        self.score += point_value
    
    def event_checks(self):
        for event in pygame.event.get():
            # print(event)
            # Game window closes
            if event.type == QUIT:
                self.running = False
            # Press escape to pause the game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if not self.game_over:
                        self.pause = not self.pause
                    else:
                        self.game_over = False
                        self.start()
            elif event.type == WINDOWFOCUSGAINED:
                self.focus_pause = False
            elif event.type == WINDOWFOCUSLOST:
                self.focus_pause = True

    def collision_checks(self, screen_size):
        '''
        collision_checks
        ~~~~~~~~~~

        collision_checks does stuff
        '''
        # Collision check between snake and food
        if self.obj_dict["snake"].rect.colliderect(self.obj_dict["food"]):
            self.obj_dict["food"].alive = False
            self.obj_dict["snake"].grow(self.obj_dict["food"])
            self.up_score(self.obj_dict["food"].point_value)
        # Collision check for edge of screen
        if (self.obj_dict["snake"].pos_x > self.screen_size[0]-self.obj_dict["snake"].size) or (
             self.obj_dict["snake"].pos_y > self.screen_size[1]-self.obj_dict["snake"].size):
            self.game_over = True
        if self.obj_dict["snake"].pos_x < 0 or self.obj_dict["snake"].pos_y < 0:
            self.game_over = True
        # Collision check between snake and tails
        i = 0
        for tail in self.obj_dict["snake"].tail_segments:
            # Skip the first tail segment
            if i > 0:
                if self.obj_dict["snake"].rect.colliderect(tail):
                    self.game_over = True
            i += 1

    def pause_menu(self):
        '''
        pause_menu
        ~~~~~~~~~~

        pause_menu does stuff
        '''
        # Render the score
        text_str = 'Score: ' + str(self.score)
        _ = self.game_font.render_to(
            self.screen,
            (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
             self.screen_size[1]/8),
            text_str,
            (255, 255, 255)
        )
        # Update the screen display
        pygame.display.update()

    def game_over_menu(self):
        '''
        game_over_menu
        ~~~~~~~~~~

        game_over_menu does stuff
        '''
        # Render the Game Over text
        text_str = 'Game Over'
        _ = self.game_font.render_to(
            self.screen,
            (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
             self.screen_size[1]/14),
            text_str,
            (255, 255, 255)
        )
        # Render the score
        text_str = 'Score: ' + str(self.score)
        _ = self.game_font.render_to(
            self.screen,
            (self.screen_size[0]/2-(len(text_str)*self.game_font.size)/2,
             self.screen_size[1]/8),
            text_str,
            (255, 255, 255)
        )
        # Update the screen display
        pygame.display.update()
