#!/usr/bin/env python3

"""
    Food

    it's the food obj

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from random import randrange
from typing import TYPE_CHECKING

from ...constants import (
    SOUND_FOOD_PICKUP_IDX,
    X,
    Y,
)

from ..entity import Entity
from ..snake import Snake

if TYPE_CHECKING:
    from ...game import Game


class Food(Entity):
    """Food

    Food for the snake
    """

    def __init__(self, game: "Game", screen_size: tuple[int, int]):
        # Name for this type of object
        self.name = "food_"

        # Initilize parent init
        super().__init__(game, screen_size, self.name)

        # Where the food is located
        x = self.screen_size[X] - randrange(
            self.game.grid_size, self.screen_size[X], self.game.grid_size
        )
        y = self.screen_size[Y] - randrange(
            self.game.grid_size, self.screen_size[Y] - self.game.game_bar_height, self.game.grid_size
        )
        self.position = (x, y)

        # Food Sprite images
        self.food_images = self.game.food_images

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
        if self.game.app.is_audio:
            self.sound_death = self.game.sounds[SOUND_FOOD_PICKUP_IDX]
            self.sound_mod = 1.5
            self.sound_death_volume = float(self.game.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        self.spawn()


    def update(self) -> bool:
        """update

        update does stuf
        """

        return self.spawn()


    def draw(self, updated_refresh: tuple[bool, bool], *kwargs) -> None:
        """draw

        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and (updated_refresh[X] or updated_refresh[Y]):
            # print(self.position, self.prev_position, self.is_alive, self.children, self.is_spawned)

            # Render the entity based on it's parameters
            self.game.screen.blit(self.image, self.position)


    def spawn(self) -> tuple[bool, bool]:
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


    def interact(self, interacting_obj: Snake) -> None:
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
