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
        super().__init__(screen, screen_size, self.name, base_game)
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
                for _, oth_obj in obj_dict.items():
                    collision_bool = self.rect.collidepoint(self.pos_x, self.pos_y)
                    if collision_bool:
                        break

                if collision_bool:
                        continue

                for _, oth_obj in obj_dict.items():
                    try:
                        if oth_obj.children:
                            self.rect.collidelist(oth_obj.children)
                    except AttributeError:
                        pass

                found_spawn = True

            self.alive = True

    def interact(self, obj1):
        if obj1.killable:
            # Play interact sound
            sound = self.sound_interact
            sound.set_volume(self.sound_interact_volume)
            pygame.mixer.Sound.play(sound)
            # Grow obj1 if obj2 is food and up obj1 score
            obj1.grow(self.screen, self)
            obj1.up_score(self)
            # Kill second obj
            self.alive = False
