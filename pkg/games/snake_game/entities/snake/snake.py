#!/usr/bin/env python3

"""
    Snake

    It's a snake

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from math import hypot as math_hypot
from typing import Deque, TYPE_CHECKING
from datetime import datetime, timedelta

from pygame import key as pygame_key

from ...ai.helpers import obj_pos_to_node
from ..entity import Entity

from ...constants import (
    COLOR_BLACK,
    INPUT_KEY_MAP,
    SOUND_SNAKE_DEATH_IDX,
    POS_IDX,
    DIST_FROM_SELF_IDX,
    ENTITY,
    CHILD,
    X,
    Y,
)

if TYPE_CHECKING:
    from ...game import Game


class Snake(Entity):
    """Snake

    obj for the snake
    """

    def __init__(self, game: "Game", is_player: bool = False):
        # Name for this type of object
        self.name = "snake_"

        # Initilize parent init
        super().__init__(game, self.name)

        # player indicator
        self.is_player = is_player

        # Where the snake was located
        # self.prev_position = (0, 0)

        # Where the snake is started located
        self.set_random_spawn(10, 10)

        # How big snake parts are
        self.size = self.game.grid_size

        # How fast the entity can move per loop-tick
        # 1 = 100%, 0 = 0%,
        self.speed_mod = 2

        # Snake Sprite images
        if self.is_player:
            self.sprite_images = self.game.snake_images
            # self.obj_color = (0, randint(100, 175), 0, 1000)
        else:
            self.sprite_images = self.game.snake_enemy_images
            # self.obj_color = (randint(100, 175), 0, 0, 1000)

        # Entity's visual representation
        self.image = self.sprite_images[0]

        # Tint the sprite with a color
        # self.tint(self.obj_color)

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Snake death sound
        if self.game.app.is_audio:
            self.sound_death = self.game.sounds[SOUND_SNAKE_DEATH_IDX]
            self.sound_mod = 4.5
            self.sound_death_volume = float(self.game.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        # Interact sound
        # if self.game.app.is_audio:
            # self.sound_interact = pygame.mixer.Sound("")

        # AI difficulty setting (higher is more difficult/smarter)
        self.ai_difficulty = self.game.game_config["settings"]["gameplay"]["ai_difficulty"]

        # Initilize the cached calculated path to target
        self.path = []

        # Entity's children/followers in a train of same children objs
        self.child_train = True

        # Number of starting tail segments
        self.num_tails = 5

        # Initilize starting tails
        self.children: Deque[TailSegment] = Deque()
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(self, self.game, player=self.is_player))
            else:
                self.children.append(TailSegment(self, self.game, player=self.is_player))


    def aquire_primary_target(self, target_name: str) -> None:
        """update

        update does stuff
        """

        # Set variables pre loop
        primary_target = (None, 10000)

        for obj in self.game.sprite_group.sprites():
            if target_name in obj.id:
                dist_self = math_hypot(obj.position[X] - self.position[X], obj.position[Y] - self.position[Y])
                if dist_self < primary_target[DIST_FROM_SELF_IDX]:
                    pos = (obj.position[X], obj.position[Y])
                    primary_target = (pos, dist_self)

        self.target = ((primary_target[POS_IDX][X], primary_target[POS_IDX][Y]), dist_self, target_name)

        self.direction = self.game.chosen_ai.decide_direction(
            self,
            self.target,
            ai_difficulty=self.ai_difficulty,
        )

        self.since_secondary_target = datetime.now()


    def update(self) -> tuple[bool, bool]:
        """update

        update does stuff
        """

        # try to choose a direction if entity can
        self.choose_direction()

        # Try to move if entity can
        is_updated = self.move()

        return is_updated, False


    def draw(self, updated_refresh: tuple[bool, bool], *kwargs) -> None:
        """
        draw


        draw does stuff
        """

        if self.state == Entity.ALIVE and (updated_refresh[ENTITY] or updated_refresh[CHILD]):

            # Tint the sprite with a color
            # self.tint(self.obj_color)

            # Render the entity's sight lines
            for line in self.sight_lines:
                line.draw()

            for line in self.sight_lines_diag:
                line.draw()

            # Render the entity's obj based on it's parameters
            self.game.screen.blit(self.image, self.position)

            if len(self.children) > 0 and self.child_train:
                # Only move/render the last child to front of the train
                self.children[-1].draw()

                # Change the new last child's image to the tail
                self.children[-1].make_end_img()


    def grow(self, eaten_obj: Entity) -> None:
        """
        grow


        grow does stuff
        """

        # Add a new tail segment
        if self.state == Entity.ALIVE:
            new_tails = Deque()

            for _ in range(eaten_obj.growth):
                tail = TailSegment(
                    self,
                    self.game,
                    player=self.is_player,
                )

                new_tails.append(tail)

                self.num_tails += 1

            self.children = self.children + new_tails


    def choose_direction(self) -> None:
        """
        choose_direction


        choose_direction does stuff
        """

        if self.state == Entity.ALIVE:
            # Check if Ai or player controls this entity
            if self.is_player:
                key = pygame_key.get_pressed()
                config = self.game.game_config["settings"]["keybindings"]
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

        move_cooldown_timer = self.time_last_moved + timedelta(milliseconds=self.base_speed/self.speed_mod)
        if datetime.now() >= move_cooldown_timer and self.state == Entity.ALIVE:
            if not self.is_player:
                # Ai makes it's decision for what direction to move
                self.aquire_primary_target("food")

            input(f"press enter to continue move {self.direction}")

            # Save current position as last position
            self.prev_position = self.position

            # Save prev_direction for child stuff
            self.child_prev_direction = self.prev_direction

            # Moving up
            if self.direction == 0:
                self.image = self.sprite_images[10]
                self.prev_direction = self.direction
                self.position = (self.position[X], self.position[Y] - self.size)

            # Moving down
            elif self.direction == 2:
                self.image = self.sprite_images[11]
                self.prev_direction = self.direction
                self.position = (self.position[X], self.position[Y] + self.size)

            # Moving left
            elif self.direction == 3:
                self.image = self.sprite_images[13]
                self.prev_direction = self.direction
                self.position = (self.position[X] - self.size, self.position[Y])

            # Moving right
            elif self.direction == 1:
                self.image = self.sprite_images[12]
                self.prev_direction = self.direction
                self.position = (self.position[X] + self.size, self.position[Y])

            # Mark previous grid position as walkable for pathfinding
            obj_pos_to_node(self.game, self.prev_position).walkable = True

            # Mark grid position as unwalkable for pathfinding
            obj_pos_to_node(self.game, self.position).walkable = False

            # Set current position for hitbox
            self.rect.topleft = self.position

            # Set the new last moved time
            self.time_last_moved = datetime.now()

            # Entity updated
            return True

        # Entity didn't update
        return False


class TailSegment(Entity):
    """TailSegment

    Tail Segment for the snake
    """

    def __init__(self, parent: Snake, game: "Game", player: bool = False):
        # Name for this type of object
        self.name = "tail-segment_"

        # Initilize parent init
        super().__init__(game, self.name)

        # The game obj
        self.game = game

        # The entity state, defaults to alive
        self.state = Entity.ALIVE

        # Parent of this child
        self.parent = parent
        self.parent_dir = parent.direction

        # Is this a entity part of the player obj?
        self.is_player = player

        # Determines if entity can be killed
        self.is_killable = False

        # No Sight lines for tail segments
        self.sight_lines = []

        # Entity's visual representation
        self.img_index = 2
        self.image = self.parent.sprite_images[self.img_index]

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Mark grid position as unwalkable for pathfinding
        obj_pos_to_node(self.game, self.position).walkable = False

        # self.obj_color = self.parent.obj_color


    def draw(self, *kwargs) -> None:
        """
        draw

        draw does stuff
        """

        # render if alive
        if self.state == Entity.ALIVE:
            # Clear previous frame obj's location
            self.game.screen.fill(COLOR_BLACK, (self.position[X], self.position[Y], self.rect.width, self.rect.height))

            # Save current position as last position
            self.prev_position = self.position

            # located where the parent obj was last
            self.position = self.parent.prev_position
            self.rect.topleft = self.position

            # Mark previous grid position as walkable for pathfinding
            obj_pos_to_node(self.game, self.prev_position).walkable = True

            # Mark grid position as unwalkable for pathfinding
            obj_pos_to_node(self.game, self.position).walkable = False

            # Choose the right image for this segment
            self.choose_img()

            # Tint the sprite with a color
            # self.tint(self.obj_color)

            # Render the tail segment based on it's parameters
            self.game.screen.blit(self.image, self.position)

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

        # Tint the sprite with a color
        # self.tint(self.obj_color)

        # Render the tail segment based on it's parameters
        self.game.screen.blit(self.image, self.position)

