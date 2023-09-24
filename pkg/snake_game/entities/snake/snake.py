#!/usr/bin/env python3

"""
    Snake

    It's a snake

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from math import hypot as math_hypot
from random import randrange
from typing import Deque
from datetime import datetime, timedelta

from pygame import (
    key as pygame_key,
    Surface,
)

from ..entity import Entity, Line
from ...constants import COLOR_BLACK, COLOR_RED, INPUT_KEY_MAP
from ....app import App


class Snake(Entity):
    """Snake

    obj for the snake
    """

    def __init__(self, screen_size: tuple[int, int], app: App, player: bool = False):
        # Name for this type of object
        self.name = "snake_"

        # Initilize parent init
        super().__init__(screen_size, self.name, app)

        # Is this the player entity
        self.player = player

        # Where the snake is started located
        x = self.screen_size[0] - randrange(
            self.app.game.grid_size, self.screen_size[0], self.app.game.grid_size
        )

        y = self.screen_size[1] - randrange(
            self.app.game.grid_size, self.screen_size[1] - self.app.game.game_bar_height - self.app.game.game_bar_height, self.app.game.grid_size
        )

        self.position = (x, y)

        # Where the snake was located
        self.prev_position = (x, y - self.app.game.grid_size)

        # How big snake parts are
        self.size = self.app.game.grid_size

        # How many moves the snake can make per second
        self.speed_mod = 2

        # head color = red
        self.obj_color = COLOR_RED

        # Snake Sprite images
        if self.player:
            self.sprite_images = self.app.game.snake_images
        else:
            self.sprite_images = self.app.game.snake_enemy_images

        # Entity's default no sprite visual representation
        self.image = Surface((self.size, self.size))
        self.image.fill(self.obj_color)

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Snake death sound
        self.sound_death = self.app.game.sounds[0]
        self.sound_mod = 4.5
        self.sound_death_volume = float(app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        # Interact sound
        # self.sound_interact = pygame.mixer.Sound("")

        # AI difficulty setting (higher is more difficult/smarter)
        self.ai_difficulty = 10

        # Entity's children/followers in a train of same children objs
        self.child_train = True

        # Number of tail segments
        self.num_tails = 5

        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(self, app, screen_size, player=self.player))
            else:
                self.children.append(TailSegment(self, app, screen_size, player=self.player))


    def aquire_primary_target(self, target_name: str) -> None:
        # Set variables pre loop
        primary_target = (None, 10000*100000)

        pos = (self.app.game.screen_size[0]/2, self.app.game.screen_size[1]/2)

        for obj in self.app.game.sprite_group.sprites():
            if target_name in obj.id:
                dist_self = math_hypot(obj.position[0] - self.position[0], obj.position[1] - self.position[1])
                if dist_self < primary_target[1]:
                    pos = (obj.position[0], obj.position[1])
                    primary_target = (pos, dist_self)

        self.target = (target_name, primary_target[0][0], primary_target[0][1])

        self.direction = self.app.game.chosen_ai.decide_direction(
            self,
            self.target,
            ai_difficulty=self.ai_difficulty,
        )

        self.since_secondary_target = datetime.now()


    def draw(self, updated_refresh: tuple[bool, bool], *kwargs) -> None:
        """
        draw


        draw does stuff
        """

        if self.is_alive and (updated_refresh[0] or updated_refresh[1]):

            # Render the entity's obj based on it's parameters
            self.app.game.screen.blit(self.image, self.position)

            # Render the entity's sight lines
            for line in self.sight_lines:
                Line.draw(line, self)

            for line in self.sight_lines_diag:
                Line.draw(line, self)

            # Draw all children on refresh or optimized one child per
            if updated_refresh[1]:
                # Draw each child if there are any
                for child in self.children:
                    child.refresh_draw()

            elif len(self.children) > 0 and self.child_train:
                # Only move/render the last child to front of the train
                self.children[-1].draw(updated_refresh)

                # Change the new last child's image to the tail
                self.children[-1].make_end_img()


    def grow(self, eaten_obj: Entity) -> None:
        """
        grow


        grow does stuff
        """

        # Add a new tail segment
        if self.is_alive:
            new_tails = Deque()

            for _ in range(eaten_obj.growth):
                tail = TailSegment(
                    self,
                    self.app,
                    self.screen_size,
                    player=self.player,
                )

                new_tails.append(tail)

                self.num_tails += 1

            self.children = self.children + new_tails


    def choose_direction(self) -> None:
        """
        choose_direction


        choose_direction does stuff
        """

        if self.is_alive:
            # Check if Ai or player controls this entity
            if self.player:
                key = pygame_key.get_pressed()
                config = self.app.game.game_config["settings"]["keybindings"]
                # pylint: disable=access-member-before-definition
                if key[INPUT_KEY_MAP[config["move_up"]]] and self.direction != 0 and self.prev_direction != 2:
                    # pylint: disable=access-member-before-definition
                    self.direction = 0

                elif key[INPUT_KEY_MAP[config["move_down"]]] and self.direction != 2 and self.prev_direction != 0:
                    self.direction = 2

                elif key[INPUT_KEY_MAP[config["move_left"]]] and self.direction != 3 and self.prev_direction != 1:
                    self.direction = 3

                elif key[INPUT_KEY_MAP[config["move_right"]]] and self.direction != 1 and self.prev_direction != 3:
                    self.direction = 1

            else:
                # Ai makes it's decision and move together
                pass


    def move(self) -> bool:
        """
        move


        move does stuff
        """

        # pylint: disable=access-member-before-definition
        if datetime.now() >= self.time_last_moved + timedelta(milliseconds=self.base_speed/self.speed_mod) and self.is_alive:
            if not self.player:
                # Ai makes it's decision for what direction to move
                self.aquire_primary_target("food")

            # pylint: disable=access-member-before-definition
            # Save current position as last position
            self.prev_position = self.position

            # Save prev_direction for child stuff
            self.child_prev_direction = self.prev_direction

            # Moving up
            if self.direction == 0:
                self.image = self.sprite_images[10]
                self.prev_direction = self.direction
                self.position = (self.position[0], self.position[1] - self.size)

            # Moving down
            elif self.direction == 2:
                self.image = self.sprite_images[11]
                self.prev_direction = self.direction
                self.position = (self.position[0], self.position[1] + self.size)

            # Moving left
            elif self.direction == 3:
                self.image = self.sprite_images[13]
                self.prev_direction = self.direction
                self.position = (self.position[0] - self.size, self.position[1])

            # Moving right
            elif self.direction == 1:
                self.image = self.sprite_images[12]
                self.prev_direction = self.direction
                self.position = (self.position[0] + self.size, self.position[1])

            # Set current position for hitbox
            self.rect.topleft = self.position

            # Set the new last moved time
            self.time_last_moved = datetime.now()

            # input("enter to continue")

            # Entity updated
            return True

        # Entity didn't update
        return False


class TailSegment(Entity):
    """TailSegment

    Tail Segment for the snake
    """

    def __init__(self, parent: Snake, app: App, screen_size: tuple[int, int], player: bool = False):
        # Name for this type of object
        self.name = "tail-segment_"

        # Initilize parent init
        super().__init__(screen_size, self.name, app)

        # Entity is dead or alive
        self.is_alive = True

        # Parent of this child
        self.parent = parent
        self.parent_dir = parent.direction

        # Is this a entity part of the player obj?
        self.player = player

        # Determines if entity can be killed
        self.killable = False

        if self.player:
            # Tail color = white
            self.obj_color = (255, 255, 255)
        else:
            # Tail color = Red   (if not a player snake)
            self.obj_color = COLOR_RED

        # No Sight lines for tail segments
        self.sight_lines = []

        # Entity's visual representation
        self.image = Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        self.img_index = 2

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)


    def draw(self, *kwargs) -> None:
        """
        draw


        draw does stuff
        """

        # render if alive
        if self.is_alive:
            # Clear previous frame obj's location
            self.app.game.screen.fill(COLOR_BLACK, (self.position[0], self.position[1], self.rect.width, self.rect.height))

            # Save current position as last position
            self.prev_position = self.position

            # located where the parent obj was last
            self.position = self.parent.prev_position
            self.rect.topleft = self.position

            # Choose the right image for this segment
            self.choose_img()

            # Render the tail segment based on it's parameters
            self.app.game.screen.blit(self.image, self.position)

            # Move the child to the front of the list
            self.parent.children.rotate()


    def choose_img(self) -> None:
        """choose_img
        """

        # Moving up
        if self.parent.direction == 0:
            if self.parent.child_prev_direction == self.parent.direction:
                self.img_index = 0
            elif self.parent.child_prev_direction == 1:
                self.img_index = 5
            elif self.parent.child_prev_direction == 3:
                self.img_index = 4

        # Moving down
        elif self.parent.direction == 2:
            if self.parent.child_prev_direction == self.parent.direction:
                self.img_index = 0
            elif self.parent.child_prev_direction == 1:
                self.img_index = 2
            elif self.parent.child_prev_direction == 3:
                self.img_index = 3

        # Moving left
        elif self.parent.direction == 3:
            if self.parent.child_prev_direction == self.parent.direction:
                self.img_index = 1
            elif self.parent.child_prev_direction == 0:
                self.img_index = 2
            elif self.parent.child_prev_direction == 2:
                self.img_index = 5

        # Moving right
        elif self.parent.direction == 1:
            if self.parent.child_prev_direction == self.parent.direction:
                self.img_index = 1
            elif self.parent.child_prev_direction == 0:
                self.img_index = 3
            elif self.parent.child_prev_direction == 2:
                self.img_index = 4

        else:
            self.img_index = self.img_index

        self.image = self.parent.sprite_images[self.img_index]
        self.parent_dir = self.parent.direction


    def make_end_img(self) -> None:
        """make_end_img
        """

        ahead_img_index = self.parent.children[-2].img_index
        if ahead_img_index in [0, 4, 5]:
            if self.parent_dir == 0:
                self.img_index = 6

            elif self.parent_dir == 1:
                self.img_index = 8

            elif self.parent_dir == 3:
                self.img_index = 9

            else:
                self.img_index = 7

        elif ahead_img_index in [1, 2, 3]:
            if self.parent_dir == 1:
                self.img_index = 8

            elif self.parent_dir == 0:
                self.img_index = 6

            elif self.parent_dir == 0:
                self.img_index = 7

            else:
                self.img_index = 9

        self.image = self.parent.sprite_images[self.img_index]

        # Render the tail segment based on it's parameters
        self.app.game.screen.blit(self.image, self.position)


    def interact(self, interacting_obj: Entity) -> None:
        """interact

        Args:
            interacting_obj ([type]): [description]
        """

        # Kill interacting_obj
        interacting_obj.die(f"collided with {self.id} and died")
