#!/usr/bin/env python3

'''
    Entities
    ~~~~~~~~~~

    All the entities in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import random
import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)
# pylint: enable=no-name-in-module

SNAKE_DEATH = 0
PICK_UP_SOUND = 1


class Snake():
    '''
    Snake
    ~~~~~~~~~~

    AI for the snake
    '''
    def __init__(self, screen, base_game):
        # Snake is dead or alive
        self.alive = True
        # Snake is player
        self.player = True
        # Score this entity has accumulated
        self.score = 0
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
        self.rect = pygame.draw.rect(screen, self.head_color, self.head)
        # Snake death sound
        self.sound_death = SNAKE_DEATH
        self.sound_death_volume = base_game.effect_volume/4.5
        # Interact sound
        # self.sound_interact = pygame.mixer.Sound("")
        # Number of tail segments
        self.num_tails = 5
        # tail segment list
        self.children = []
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(screen, self, pos))
            else:
                self.children.append(TailSegment(screen, self.children[pos-1], pos))

    def draw(self, screen):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Draw each tail
            for tail in self.children:
                tail.draw(screen)
             # head pos/size  = (left, top, width, height)
            self.head = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the snake's head based on it's parameters
            self.rect = pygame.draw.rect(screen, self.head_color, self.head)

    def grow(self, screen, food):
        '''
        grow
        ~~~~~~~~~~

        grow does stuff
        '''
        # Add a new tail segment
        for _ in range(food.growth):
            self.children.append(TailSegment(
                screen,
                self.children[self.num_tails - 1],
                self.num_tails + 1
            ))
            self.num_tails += 1

    def up_score(self, point_value):
        '''
        up_score
        ~~~~~~~~~~

        up_score does stuff
        '''
        # Increase the score
        self.score += point_value

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
        if self.moved_last_cnt > self.speed and self.alive:
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
        # Tail is dead or alive
        self.alive = True
        # tail segment isn't player
        self.player = False
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
        self.rect = pygame.draw.rect(screen, self.tail_color, self.tail)

    def draw(self, screen):
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
            self.rect = pygame.draw.rect(screen, self.tail_color, self.tail)


class Food():
    '''
    Food
    ~~~~~~~~~~

    Food for the snake
    '''
    def __init__(self, screen, screen_size, base_game):
        # Food is dead or alive
        self.alive = False
        # food isn't player
        self.player = False
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
        self.rect = pygame.draw.rect(screen, self.food_color, self.food)
        # How much a snake grows from eating food
        self.growth = 5
        # Point value of the food
        self.point_value = 10
        # Interact sound
        self.sound_interact = PICK_UP_SOUND
        self.sound_interact_volume = base_game.effect_volume/1.5
        self.children = None

    def draw(self, screen):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # food pos/size = (left, top, width, height)
            self.food = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the food segment based on it's parameters
            self.rect = pygame.draw.rect(screen, self.food_color, self.food)

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
            # print(obj_dict["food1"])
            collision_objs = obj_dict["food1"].rect.collidedictall(obj_dict, 1)
            if len(collision_objs) < 1:
                continue
            for _, obj in obj_dict.items():
                try:
                    if obj.children:
                        obj_dict["food1"].rect.collidelist(obj.children)
                except AttributeError:
                    pass
            found_spawn = True

        self.alive = True
