#!/usr/bin/env python3

'''
    Snake
    ~~~~~~~~~~

    It's a snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

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
        self.movement = 2
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
        # Number of tail segments
        self.num_tails = 5
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(alpha_screen, screen, screen_size, app, self, pos, self.ID, player=self.player))
            else:
                self.children.append(TailSegment(alpha_screen, screen, screen_size, app, self.children[pos-1], pos, self.ID, player=self.player))

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
                    parent_id = self.ID,
                    player=self.player,
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
                # Ai makes it's decision and move together
                pass

    def move(self):
        '''
        move
        ~~~~~~~~~~

        move does stuff
        '''
        # pylint: disable=access-member-before-definition
        if datetime.now() >= self.time_last_moved + timedelta(milliseconds=self.base_speed/self.movement) and self.alive:
            if not self.player:
                # Ai makes it's decision for what direction to move
                self.aquire_primary_target("food")
            # pylint: disable=access-member-before-definition
            # Save current position as last position
            self.prev_position = self.position
            print(f"Direction: {self.direction}")
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


class TailSegment(Entity):
    '''
    TailSegment
    ~~~~~~~~~~

    Tail Segment for the snake
    '''
    def __init__(self, alpha_screen, screen, screen_size, app, ahead_obj, tail_pos, parent_id, player=False):
        # Name for this type of object
        self.name = "tail-segment_"
        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)
        # Entity is dead or alive
        self.alive = True
        # Parent of this child
        self.parent_id = parent_id
        # Is this a entity part of the player obj?
        self.player = player
        # Determines if entity can be killed
        self.killable = False
        # Obj ahead of this obj in the chain of tails/head
        self.ahead_obj = ahead_obj
        # Position in the chain of tails/head
        self.tail_pos = tail_pos
        # Where the tail was/is located
        prev_x = ahead_obj.position[0] # was
        prev_y = None
        x = ahead_obj.prev_position[0] # is
        y = None
        if tail_pos == 0:
            prev_y = ahead_obj.position[1]-self.size # was
            y = ahead_obj.prev_position[1]-self.size # is
        else:
            prev_y = ahead_obj.prev_position[1] # was
            y = ahead_obj.prev_position[1] # is
        self.prev_position = (prev_x, prev_y)
        self.position = (x, y)
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

    def draw(self, screen, _):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Save current position as last position
            self.prev_position = self.position
            # located where the ahead obj was last
            self.position = self.ahead_obj.prev_position
            # Render the tail segment based on it's parameters
            screen.blit(self.image, self.position)

    def interact(self, interacting_obj):
        # Skip the first tail segment for interaction with it's head
        if interacting_obj.ID == self.parent_id and self.tail_pos == 0:
            print(f"Avoiding hitting head")
            return
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
