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
)
# pylint: enable=no-name-in-module


class SnakeAI():
    '''
    SnakeAI
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
        self.prev_direction = 1
        # Where snake is looking = (North = 0, East = 1, South = 2, West = 3)
        self.direction = 1
        # Determines how far the snake can see ahead of itself in the direction it's looking
        self.sight = 5
        # head pos/size  = (left, top, width, height)
        self.head = (self.pos_x, self.pos_y, self.size+8, self.size)
        self.rect = None
        # head color = red
        self.head_color = (255, 0, 0)
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
        for i in range(food.growth):
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
        self.prev_direction = self.direction
        if key[K_UP]:
            self.direction = 0
        elif key[K_DOWN]:
            self.direction = 2
        elif key[K_LEFT]:
            self.direction = 3
        elif key[K_RIGHT]:
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
            if self.direction == 0 and not self.prev_direction == 2:
                self.pos_y -= self.size
            # Moving down
            elif self.direction == 2 and not self.prev_direction == 0:
                self.pos_y += self.size
            # Moving left
            elif self.direction == 3 and not self.prev_direction == 1:
                self.pos_x -= self.size
            # Moving right
            elif self.direction == 1 and not self.prev_direction == 3:
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
        # Where the tail was located
        self.prev_pos_x = ahead_obj.pos_x
        self.prev_pos_y = ahead_obj.pos_y-self.size
        # Where the tail is located
        self.pos_x = ahead_obj.pos_x
        self.pos_y = ahead_obj.pos_y-self.size
        # tail pos/size = (left, top, width, height)
        self.tail = (self.pos_x, self.pos_y, self.size+8, self.size)
        self.rect = None
        # tail color = white
        self.tail_color = (255, 255, 255)

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

        self.alive = True=


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
        self.size = (screen_w, screen_h)
        self.score = 0

    def play(self):
        '''
        play
        ~~~~~~~~~~

        play does stuff
        '''

        clock = pygame.time.Clock()

        # Initilize game objects
        food = Food(self.screen, self.size)
        snake = SnakeAI(self.screen)

        # Game loop
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                # Game window closes
                if event.type == QUIT:
                    running = False
                # Press escape to pause the game
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = not pause
            # Game is paused
            if not pause:
                # Clear previous frame render
                self.screen.fill((0, 0, 0, 0))

                # Spawn a new food after it's eaten
                if not food.alive:
                    food.spawn()

                ## Draw game Objects
                food.draw()
                snake.draw()
                pygame.display.update()

                ## Game logic
                # Snake control and movement
                snake.choose_direction()
                snake.move()
                # Collision check between snake and food
                if snake.rect.colliderect(food):
                    food.alive = False
                    snake.grow(food)
                    self.up_score()
            else:
                textsurface = self.game_font.render(
                    'Score: ' + str(self.score),
                    True,
                    (255, 255, 255)
                )
                self.screen.blit(textsurface, (0, 0))

            # The game loop FPS
            clock.tick(60)

        # pylint: disable=no-member
        pygame.quit()
        # pylint: enable=no-member

    def up_score(self):
        self.score += 10
