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
# pylint: disable=relative-beyond-top-level
from ..entity import Entity
# pylint: enable=relative-beyond-top-level


class Food(Entity):
    '''
    Food
    ~~~~~~~~~~

    Food for the snake
    '''
    def __init__(self, screen, screen_size, base_game):
        # Name for this type of object
        self.name = "food_"
        # Initilize parent init
        super().__init__(screen, screen_size, self.name)
        # Where the food is located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        # Food color = green
        self.obj_color = (0, 255, 0)
        # How much an obj grows from eating this food
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
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the food segment based on it's parameters
            self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)

    def spawn(self, obj_dict):
        '''
        spawn
        ~~~~~~~~~~

        spawn does stuff
        '''
        found_spawn = False
        # pylint: disable=access-member-before-definition
        if not self.alive:
            # pylint: enable=access-member-before-definition
            while not found_spawn:
                # Where the food is located
                self.pos_x = self.screen_size[0] - random.randrange(
                    16, self.screen_size[0], 16
                )
                self.pos_y = self.screen_size[1] - random.randrange(
                    16, self.screen_size[1], 16
                )
                # Check if the chosen random spawn location is taken
                collision_objs = obj_dict[self.ID].rect.collidedictall(obj_dict, 1)
                if len(collision_objs) < 1:
                    continue
                for _, oth_obj in obj_dict.items():
                    try:
                        if oth_obj.children:
                            obj_dict[self.ID].rect.collidelist(oth_obj.children)
                    except AttributeError:
                        pass
                found_spawn = True

        self.alive = True
