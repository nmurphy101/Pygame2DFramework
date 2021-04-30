#!/usr/bin/env python3

'''
    Entitie
    ~~~~~~~~~~

    Base entity in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import uuid
import pygame


class Entity():
    '''
    Entity
    ~~~~~~~~~~

    base obj for all entities
    '''
    def __init__(self, screen, screen_size, name):
        # Unique identifier
        self.ID = name + str(uuid.uuid4())
        # Entity is dead or alive
        self.alive = True
        # Entity is player
        self.player = False
        # Score this entity has accumulated
        self.score = 0
        # Where the entity was located
        self.prev_pos_x = -20
        self.prev_pos_y = -20
        # Size of the game screen
        self.screen_size = screen_size
        # Where the entity is located
        self.pos_x = -20
        self.pos_y = -20
        # How big entity is
        self.size = 16
        # How fast the entity can move per loop-tick
        self.speed = 1
        self.moved_last_cnt = 0
        # Where entity was looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.prev_direction = 2
        # Where entity is looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.direction = 2
        # Determines how far the entity can see ahead of itself in the direction it's looking
        self.sight = 5
        # Obj pos/size  = (left, top, width, height)
        self.obj = (self.pos_x, self.pos_y, self.size+8, self.size)
        # RGB color = pink default
        self.obj_color = (255,105,180)
        # Entity is a rectangle object
        self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)
        # children list
        self.children = []

    def draw(self, screen, obj_dict):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Draw each child if there are any
            if self.children:
                for child in self.children:
                    child.draw(screen)
             # obj pos/size  = (left, top, width, height)
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the entity's obj based on it's parameters
            self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)
