#!/usr/bin/env python3

'''
    Snake
    ~~~~~~~~~~

    It's a snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import random
from typing import Deque
from datetime import datetime, timedelta
import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)
# pylint: enable=no-name-in-module
# pylint: disable=relative-beyond-top-level
from ..entity import Entity, Line
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
        x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        self.position = (x, y)
        # Where the snake was located
        self.prev_position = (x, y - 16)
        # How big snake parts are
        self.size = 16
        # How many moves the snake can make per second
        self.speed_mod = 2
        # head color = red
        self.obj_color = (255, 0, 0)
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)
        # Snake death sound
        self.sound_death = self.app.game.sounds[0]
        self.sound_mod = 4.5
        self.sound_death_volume = float(app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        # Interact sound
        # self.sound_interact = pygame.mixer.Sound("")
        # Dirty rect or not
        self.dirty_rect = True
        # Entity's children/followers in a train of same children objs
        self.child_train = True
        # Number of tail segments
        self.num_tails = 5
        # Initilize starting tails
        append = self.children.append # eval func only once
        for pos in range(self.num_tails+1):
            if pos == 0:
                append(TailSegment(alpha_screen, screen, screen_size, app, pos, self, player=self.player))
            else:
                append(TailSegment(alpha_screen, screen, screen_size, app, pos, self, player=self.player))

    def draw(self, obj_container, updated_refresh):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''

        if self.alive and (updated_refresh[0] or updated_refresh[1]):
            # Clear previous frame obj's location
            self.screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            # Set current position for hitbox
            self.rect.topleft = self.position
            # Render the entity's obj based on it's parameters
            self.screen.blit(self.image, self.position)
            # eval func's only once before loop
            draw = Line.draw
            append_dirty_rects = self.app.game.dirty_rects.append
            # Render the entity's sight lines
            for line in self.sight_lines:
                draw(line, self)
            # Draw all children on refresh or optimized one child per
            if updated_refresh[1]:
                # Draw each child if there are any
                for child in self.children:
                    append_dirty_rects(child)
                    child.refresh_draw()
            elif len(self.children) > 0 and self.child_train:
                # Add this child to the dirty rects
                append_dirty_rects(self.children[-1])
                # Only move/render the last child to front of the train
                self.children[-1].draw(obj_container, updated_refresh)

    def grow(self, eaten_obj):
        '''
        grow
        ~~~~~~~~~~

        grow does stuff
        '''
        # Add a new tail segment
        if self.alive:
            new_tails = Deque()
            for _ in range(eaten_obj.growth):
                tail = TailSegment(
                    self.alpha_screen,
                    self.screen,
                    self.screen_size,
                    self.app,
                    1,
                    parent = self,
                    player=self.player,
                )
                new_tails.append(tail)
                self.num_tails += 1
            self.children = self.children + new_tails


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
                # Ai makes it's decision and move together
                pass

    def move(self):
        '''
        move
        ~~~~~~~~~~

        move does stuff
        '''
        # pylint: disable=access-member-before-definition
        if datetime.now() >= self.time_last_moved + timedelta(milliseconds=self.base_speed/self.speed_mod) and self.alive:
            if not self.player:
                # Ai makes it's decision for what direction to move
                self.aquire_primary_target("food")
            # pylint: disable=access-member-before-definition
            # Save current position as last position
            self.prev_position = self.position
            # Moving up
            if self.direction == 0:
                self.prev_direction = self.direction
                self.position = (self.position[0], self.position[1] - self.size)
            # Moving down
            elif self.direction == 2:
                self.prev_direction = self.direction
                self.position = (self.position[0], self.position[1] + self.size)
            # Moving left
            elif self.direction == 3:
                self.prev_direction = self.direction
                self.position = (self.position[0] - self.size, self.position[1])
            # Moving right
            elif self.direction == 1:
                self.prev_direction = self.direction
                self.position = (self.position[0] + self.size, self.position[1])
            # Set the new last moved time
            self.time_last_moved = datetime.now()
            # Entity updated
            return True
        # Entity didn't update
        return False


class TailSegment(Entity):
    '''
    TailSegment
    ~~~~~~~~~~

    Tail Segment for the snake
    '''
    def __init__(self, alpha_screen, screen, screen_size, app, tail_pos, parent, player=False):
        # Name for this type of object
        self.name = "tail-segment_"
        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)
        # Entity is dead or alive
        self.alive = True
        # Parent of this child
        self.parent = parent
        # Is this a entity part of the player obj?
        self.player = player
        # Determines if entity can be killed
        self.killable = False
        # Position in the chain of tails/head
        self.tail_pos = tail_pos
        # Where the tail was/is located
        # prev_x = ahead_obj.position[0] # was
        # prev_y = None
        # x = ahead_obj.prev_position[0] # is
        # y = None
        # if tail_pos == 0:
        #     prev_y = ahead_obj.position[1]-self.size # was
        #     y = ahead_obj.prev_position[1]-self.size # is
        # else:
        #     prev_y = ahead_obj.prev_position[1] # was
        #     y = ahead_obj.prev_position[1] # is
        # self.prev_position = (prev_x, prev_y)
        # self.position = (x, y)
        if self.player:
            # Tail color = white
            self.obj_color = (255, 255, 255)
        else:
            # Tail color = Red   (if not a player snake)
            self.obj_color = (255, 0, 0)
        # No Sight lines for tail segments
        self.sight_lines = []
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)
        #
        self.child_train = None

    def draw(self, _, __):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        # render if alive
        if self.alive:
            # Clear previous frame obj's location
            self.screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            # Save current position as last position
            self.prev_position = self.position
            # located where the parent obj was last
            self.position = self.parent.prev_position
            self.rect.topleft = self.position
            # Render the tail segment based on it's parameters
            self.screen.blit(self.image, self.position)
            # Move the child to the front of the list
            self.parent.children.rotate()

    def interact(self, interacting_obj):
        # Play interacting_obj death sound
        sound = interacting_obj.sound_death
        interacting_obj.sound_death_volume = float(self.app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        sound.set_volume(interacting_obj.sound_death_volume)
        pygame.mixer.Sound.play(sound)
        # Loose the game if interacting_obj is the player
        if interacting_obj.player:
            self.app.game.menu.menu_option = 3
        # Kill interacting_obj
        interacting_obj.die(f"collided with {self.ID} and died")
