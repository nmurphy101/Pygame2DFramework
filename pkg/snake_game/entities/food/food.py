#!/usr/bin/env python3

"""
    Food

    it's the food obj

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import random
import pygame

from ..entity import Entity


class Food(Entity):
    """Food

    Food for the snake
    """

    def __init__(self, alpha_screen, screen, screen_size, app):
        # Name for this type of object
        self.name = "food_"

        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)

        # Where the food is located
        x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        self.position = (x, y)

        # Food color green
        self.obj_color = (0, 255, 0)

        # Food Sprite images
        self.food_images = self.app.game.food_images

        # Entity's visual representation
        self.image = self.food_images[0]

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # spawned
        self.is_spawned = False

        # How much an obj grows from eating this food
        self.growth = 5

        # Point value of the food
        self.point_value = 10

        # No Sight lines for tail segments
        self.sight_lines = []

        # Death sound
        self.sound_death = self.app.game.sounds[1]
        self.sound_mod = 1.5
        self.sound_death_volume = float(app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        self.spawn()


    def update(self):
        """update

        update does stuf
        """

        return self.spawn()


    def draw(self, updated_refresh, *kwargs):
        """draw

        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and (updated_refresh[0] or updated_refresh[1]):
            # print(self.position, self.prev_position, self.is_alive, self.children, self.is_spawned)

            # Clear previous frame obj's location
            # self.screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

            # Render the entity based on it's parameters
            self.screen.blit(self.image, self.position)


    def spawn(self):
        """spawn

        spawn does stuff
        """

        if not self.is_spawned:
            self.set_random_spawn()
            self.is_spawned = True
            self.is_alive = True

            updated_child = False

            if self.children:
                for child in self.children:
                    child.spawn()
                updated_child = True

            return True, updated_child

        return False, False


    def interact(self, interacting_obj):
        """interact

        Args:
            interacting_obj ([type]): [description]
        """

        # Grow interacting_obj and up interacting_obj's score
        interacting_obj.grow(self)
        interacting_obj.up_score(self)

        # Kill self
        self.is_spawned = False
        self.die(f"Eaten by {interacting_obj.id}")
        self.is_alive = True
