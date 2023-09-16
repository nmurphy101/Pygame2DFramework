#!/usr/bin/env python3

"""
    Food
    ~~~~~~~~~~

    it's the food obj


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import random
import pygame

from ..entity import Entity


class Food(Entity):
    """
    Food
    ~~~~~~~~~~

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
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # How much an obj grows from eating this food
        self.growth = 5

        # Point value of the food
        self.point_value = 10

        # No Sight lines for tail segments
        self.sight_lines = []

        # Death sound
        self.sound_death = self.app.game.sounds[1]
        self.sound_mod = 1.5
        self.sound_death_volume = float(app.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod


    def update(self, obj_container):
        # try to spawn if obj can
        updated = self.spawn(obj_container)
        return updated


    def draw(self, *kwargs):
        """
        draw
        ~~~~~~~~~~

        draw does stuff
        """

        # render if alive
        if self.alive:
            # place hitbox at position
            self.rect.topleft = self.position

            # Choose the correct image
            self.image = self.food_images[0]

            # Render the tail segment based on it's parameters
            self.screen.blit(self.image, self.position)


    def interact(self, obj1):
        # Grow obj1 and up obj1's score
        obj1.grow(self)
        obj1.up_score(self)

        # Kill self
        self.die(f"Eaten by {obj1.ID}")
