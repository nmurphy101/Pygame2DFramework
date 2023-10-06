#!/usr/bin/env python3

"""
    Teleport Portal

    It's a portal that can connect to another portal elsewhere

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from random import randint, randrange
from datetime import datetime, timedelta
from typing import Deque, TYPE_CHECKING

from pygame import mixer

from ..entity import Entity

from ...constants import (
    COLOR_BLACK,
    SOUND_PORTAL_ENTER_IDX,
    X,
    Y,
    UP,
    RIGHT,
    DOWN,
    LEFT,
)
if TYPE_CHECKING:
    from ...game import Game


class TelePortal(Entity):
    """TelePortal

    Teleport portal that entities can use to go to a connected portal elsewhere
    """

    def __init__(self, game: "Game", screen_size: tuple[int, int], parent: "TelePortal" = None):
        self.name = "teleportal_"

        # Initilize parent init
        super().__init__(game, screen_size, self.name)

        # Determines if entity can be killed
        self.is_killable = False

        # Ability cooldown timer
        self.abilty_cooldown = 1

        # Parent obj (means self is a child of said parent)
        self.parent = parent

        # spawned
        self.is_spawned = True

        # When obj should be spawned
        now = datetime.now()
        self.spawn_timer = now + timedelta(seconds=randint(2, 5))

        # Where the portal is located
        x_pos = self.screen_size[X] - randrange(
            self.game.grid_size, self.screen_size[X], self.game.grid_size
        )
        y_pos = self.screen_size[Y] - randrange(
            self.game.grid_size, self.screen_size[Y] - self.game.game_bar_height, self.game.grid_size
        )
        self.position = (x_pos, y_pos)

        # teleportation portal Sprite images
        self.tele_portal_images = self.game.tele_portal_images

        # Entity's visual representation
        self.image = self.tele_portal_images[0]

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Interact sound
        if self.game.app.is_audio:
            self.sound_interact = self.game.sounds[SOUND_PORTAL_ENTER_IDX]
            self.sound_mod = 2.5
            effect_volume = self.game.app.app_config["settings"]["sound"]["effect_volume"]
            self.sound_interact_volume = float(effect_volume)/self.sound_mod

        # Active trigger
        self.activated = now

        # No Sight lines for tail segments
        self.sight_lines = []

        # Initilize starting children if it has no parent (and thus is the parent)
        self.children: Deque[TelePortal]
        if not parent:
            self.children.append(TelePortal(game, screen_size, parent=self))

        self.spawn()


    def update(self) -> tuple[bool, bool]:
        # Verify if teleporter should be spawned
        now = datetime.now()
        if not self.is_spawned:
            pass
        elif now < self.spawn_timer:
            return False, False

        # teleporter is now spawned
        self.is_spawned = True

        # Set next spawn time
        self.spawn_timer = now + timedelta(seconds=randint(10, 25))

        # Mark previous position
        self.prev_position = self.position

        # try to spawn if obj can
        return self.spawn(), True


    def draw(self, updated_refresh: tuple[bool, bool], *kwargs) -> None:
        """
        draw

        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and (updated_refresh[X] or updated_refresh[Y]):
            # print(self.position, self.prev_position, self.is_alive, self.children)

            # Render the teleportal based on it's parameters
            self.game.screen.blit(self.image, self.position)

            # Draw each child if there are any
            for child in self.children:
                child.draw(updated_refresh)


    def spawn(self) -> tuple[bool, bool]:
        """
        spawn

        spawn does stuff
        """

        # Clear previous frame obj's location
        self.game.screen.fill(COLOR_BLACK, (self.position[X], self.position[Y], self.rect.width, self.rect.height))

        self.set_random_spawn()

        self.is_alive = True

        updated_child = False

        if self.children:
            for child in self.children:
                child.spawn()
            updated_child = True

        return True, updated_child


    def teleport(self, other_obj: Entity) -> None:
        """
        teleport

        teleport does stuff
        """

        side_num_x, side_num_y = self._determine_side(other_obj)

        # Is the child portal cuz has a parent
        if self.parent:
            # move other_obj to the parent portal
            other_obj.position = (self.parent.position[X]+side_num_x, self.parent.position[Y]+side_num_y)
            self.parent.activated = datetime.now()

        # Is the parent portal cuz doesn't have a parent
        else:
            # move other_obj to the child portal
            other_obj.position = (self.children[0].position[X]+side_num_x, self.children[0].position[Y]+side_num_y)
            self.children[0].activated = datetime.now()

        self.activated = datetime.now()


    def _determine_side(self, other_obj: Entity) -> tuple[int, int]:
        if other_obj.direction == UP:
            return 0, -self.game.grid_size
        elif other_obj.direction == RIGHT:
            return self.game.grid_size, 0
        elif other_obj.direction == DOWN:
            return 0, self.game.grid_size
        elif other_obj.direction == LEFT:
            return -self.game.grid_size, 0


    def interact(self, interacting_obj: Entity) -> None:
        """
        interact

        interact does stuff
        """

        if self.activated + timedelta(seconds=self.abilty_cooldown) <= datetime.now():
            # teleport not on cooldown
            self.activated = datetime.now()

        else:
            # Teleport on cooldown
            self.refresh_draw()
            return

        # Play second interacting_obj's interact sound
        if self.game.app.is_audio:
            sound = self.sound_interact
            effect_volume = self.game.app.app_config["settings"]["sound"]["effect_volume"]
            self.sound_interact_volume = float(effect_volume)/self.sound_mod
            sound.set_volume(self.sound_interact_volume)
            mixer.Sound.play(sound)

        # Teleport the obj to the paired portal
        self.teleport(interacting_obj)

        self.refresh_draw()
