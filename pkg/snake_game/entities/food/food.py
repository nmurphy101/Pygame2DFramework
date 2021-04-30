#!/usr/bin/env python3

'''
    Food
    ~~~~~~~~~~

    it's the food obj


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import random
import pygame

PICK_UP_SOUND = 1


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
        self.sound_interact = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav")
        self.sound_interact_volume = base_game.effect_volume/1.5
        self.children = None

    def draw(self, screen, obj_dict):
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
        else:
            # Spawn a new food after it's eaten
            self.spawn(obj_dict)

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
