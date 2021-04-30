#!/usr/bin/env python3

'''
    Teleport Portal
    ~~~~~~~~~~

    a portal that can connect to another portal elsewhere


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import random
import pygame
# pylint: disable=relative-beyond-top-level
from ..entity import Entity
# pylint: enable=relative-beyond-top-level


class TelePortal(Entity):
    '''
    TelePortal
    ~~~~~~~~~~

    Teleport portal that objects can use to go to a connected portal elsewhere
    '''
    def __init__(self, screen, screen_size, base_game, parent=False):
        self.name = "portal_"
        # Initilize parent init
        super().__init__(screen, screen_size)
        # Where the portal is located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        # TelePortal color = blue
        self.obj_color = (0, 0, 255)
        # Interact sound
        self.sound_interact = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav")
        self.sound_interact_volume = base_game.effect_volume/1.5
        # Initilize starting children if it has no parent (and thus is the parent)
        if not parent:
            self.children.append(TelePortal(screen, screen_size, base_game, parent=self))

    def draw(self, screen, obj_dict):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # portal pos/size = (left, top, width, height)
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the portal segment based on it's parameters
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
                # Where the portal is located
                self.pos_x = self.screen_size[0] - random.randrange(
                    16, self.screen_size[0], 16
                )
                self.pos_y = self.screen_size[1] - random.randrange(
                    16, self.screen_size[1], 16
                )
                # Check if the chosen random spawn location is taken
                collision_objs = obj_dict["portal1"].rect.collidedictall(obj_dict, 1)
                if len(collision_objs) < 1:
                    continue
                for _, oth_obj in obj_dict.items():
                    try:
                        if oth_obj.children:
                            obj_dict["portal1"].rect.collidelist(oth_obj.children)
                    except AttributeError:
                        pass
                found_spawn = True

        self.alive = True