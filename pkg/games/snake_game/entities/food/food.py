#!/usr/bin/env python3

"""
    Food

    it's the food obj

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from random import randrange
from typing import TYPE_CHECKING

from pkg.games.snake_game.constants import (
    SOUND_FOOD_PICKUP_IDX,
    TOP,
    ENTITY,
    CHILD,
    X,
    Y,
)

from pkg.games.snake_game.entities import Entity, Snake

if TYPE_CHECKING:
    from pkg.games.snake_game.game import SnakeGame


class Food(Entity):
    """Food

    Food for the snake
    """

    def __init__(self, game: "SnakeGame"):
        # Name for this type of object
        self.name = "food_"

        # Initilize parent init
        super().__init__(game, self.name)

        # Food Sprite images
        self.food_images = self.game.food_images

        # Entity's visual representation
        self.image = self.food_images[0]

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

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


    def update(self) -> bool:
        """update

        update does stuf
        """

        return self.spawn()


    def draw(self, updated_refresh: tuple[bool, bool], *kwargs) -> None:
        """draw

        draw does stuff
        """

        # render if alive and was updated
        if self.state == Entity.ALIVE and (updated_refresh[ENTITY] or updated_refresh[CHILD]):

            # Render the entity based on it's parameters
            self.game.screen.blit(self.image, self.position)


    def spawn(self) -> tuple[bool, bool]:
        """spawn

        spawn does stuff
        """

        if not self.is_spawned:
            self.set_random_spawn(5, 5, mod_walkability=False)
            self.is_spawned = True
            self.state = Entity.ALIVE

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
        self.state = Entity.ALIVE
