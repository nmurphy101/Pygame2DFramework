#!/usr/bin/env python3

'''
    Snake
    ~~~~~~~~~~

    It's a snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import math
import random
from datetime import datetime, timedelta
import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)
# pylint: enable=no-name-in-module
# pylint: disable=relative-beyond-top-level
from ..entity import Entity
from ...ai.ai import DecisionBox
# pylint: enable=relative-beyond-top-level

SNAKE_DEATH = 0


class Snake(Entity):
    '''
    Snake
    ~~~~~~~~~~

    obj for the snake
    '''
    def __init__(self, alpha_screen, screen, screen_size, app, player=False):
        # Name for this type of object
        self.name = "snake_"
        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)
        # Default set snake to alive
        self.alive = True
        # Make snake invinsible
        # self.killable = False
        # Is this the player entity
        self.player = player
        # Where the snake is started located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        # Where the snake was located
        self.prev_pos_x = self.pos_x
        self.prev_pos_y = self.pos_y - 16
        # How big snake parts are
        self.size = 16
        # How many moves the snake can make per second
        self.movement = 2
        # head color = red
        self.obj_color = (255, 0, 0)
        # Snake death sound
        self.sound_death = self.app.game.sounds[0]
        self.sound_mod = 4.5
        self.sound_death_volume = float(app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        # Interact sound
        # self.sound_interact = pygame.mixer.Sound("")
        # Number of tail segments
        self.num_tails = 5
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(alpha_screen, screen, screen_size, app, self, pos, player=self.player))
            else:
                self.children.append(TailSegment(alpha_screen, screen, screen_size, app, self.children[pos-1], pos, player=self.player))

    def grow(self, eaten_obj):
        '''
        grow
        ~~~~~~~~~~

        grow does stuff
        '''
        # Add a new tail segment
        if self.alive:
            for _ in range(eaten_obj.growth):
                tail = TailSegment(
                    self.alpha_screen,
                    self.screen,
                    self.screen_size,
                    self.app,
                    self.children[self.num_tails - 1],
                    self.num_tails + 1,
                    player=self.player
                )
                tail.player = self.player
                self.children.append(tail)
                self.num_tails += 1

    def up_score(self, eaten_obj):
        '''
        up_score
        ~~~~~~~~~~

        up_score does stuff
        '''
        # Increase the score
        if self.alive:
            # pylint: disable=no-member
            self.score += eaten_obj.point_value
            # pylint: enable=no-member

    def choose_direction(self):
        '''
        choose_direction
        ~~~~~~~~~~

        choose_direction does stuff
        '''
        if self.alive:
            # Check if Ai or player controls this entity
            if self.player:
                key = pygame.key.get_pressed()
                # pylint: disable=access-member-before-definition
                if key[K_UP] and self.direction != 0 and self.prev_direction != 2:
                    # pylint: disable=access-member-before-definition
                    self.direction = 0
                elif key[K_DOWN] and self.direction != 2 and self.prev_direction != 0:
                    self.direction = 2
                elif key[K_LEFT] and self.direction != 3 and self.prev_direction != 1:
                    self.direction = 3
                elif key[K_RIGHT] and self.direction != 1 and self.prev_direction != 3:
                    self.direction = 1
            else:
                # Ai makes it's decisions on the move step
                pass

    def move(self):
        '''
        move
        ~~~~~~~~~~

        move does stuff
        '''
        # pylint: disable=access-member-before-definition
        if datetime.now() >= self.time_last_moved + timedelta(milliseconds=self.base_speed/self.movement) and self.alive:
            # Check if Ai or player controls this entity
            if not self.player:
                self.aquire_primary_target("food")
            # pylint: disable=access-member-before-definition
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
            # Set the new last moved time
            self.time_last_moved = datetime.now()

    def interact_children(self, obj1):
        i = 0
        if self.children:
            for child in self.children:
                if child.alive:
                    # Skip the first tail segment
                    if i == 0:
                        i += 1
                        continue
                    if obj1.rect.colliderect(child):
                        obj1.die(f"Collided with {child.ID}")

    def aquire_primary_target(self, target_name):
        primary_target = (None, 10000*100000)
        for obj in self.app.game.obj_container:
            if target_name in obj.ID:
                dist_self = math.hypot(obj.pos_x - self.pos_x, obj.pos_y - self.pos_y)
                if dist_self < primary_target[1]:
                    primary_target = (obj, dist_self)
        self.target = (primary_target[0].pos_x, primary_target[0].pos_y)
        self.direction = self.app.game.chosen_ai.decide_direction(
            self, self.target, self.app.game.obj_container, difficulty=0
        )


class TailSegment(Entity):
    '''
    TailSegment
    ~~~~~~~~~~

    Tail Segment for the snake
    '''
    def __init__(self, alpha_screen, screen, screen_size, app, ahead_obj, position, player=False):
        # Name for this type of object
        self.name = "tail-segment_"
        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)
        # Entity is dead or alive
        self.alive = True
        # Is this a entity part of the player obj?
        self.player = player
        # Determines if entity can be killed
        self.killable = False
        # Obj ahead of this obj in the chain of tails/head
        self.ahead_obj = ahead_obj
        # Position in the chain of tails/head
        self.position = position
        # Where the tail was/is located
        self.prev_pos_x = ahead_obj.pos_x # was
        self.pos_x = ahead_obj.prev_pos_x # is
        if position == 0:
            self.prev_pos_y = ahead_obj.pos_y-self.size # was
            self.pos_y = ahead_obj.prev_pos_y-self.size # is
        else:
            self.prev_pos_y = ahead_obj.prev_pos_y # was
            self.pos_y = ahead_obj.prev_pos_y # is
        if self.player:
            # Tail color = white
            self.obj_color = (255, 255, 255)
        else:
            # Tail color = Red   (if not a player snake)
            self.obj_color = (255, 0, 0)
        # No Sight lines for tail segments
        self.sight_lines = []

    def draw(self, screen, _):
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
            # Render the tail segment based on it's parameters
            self.rect.topleft = (self.pos_x, self.pos_y)
            screen.blit(self.image, self.position)
