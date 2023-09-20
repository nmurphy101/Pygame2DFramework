#!/usr/bin/env python3

"""
    Teleport Portal

    It's a portal that can connect to another portal elsewhere

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import random
from datetime import datetime, timedelta

import pygame

from ..entity import Entity


class TelePortal(Entity):
    """TelePortal

    Teleport portal that entities can use to go to a connected portal elsewhere
    """

    def __init__(self, alpha_screen, screen, screen_size, app, parent=None):
        self.name = "teleportal_"

        # Initilize parent init
        super().__init__(alpha_screen, screen, screen_size, self.name, app)

        # Determines if entity can be killed
        self.killable = False

        # Ability cooldown timer
        self.abilty_cooldown = 1

        # Parent obj (means self is a child of said parent)
        self.parent = parent

        # spawned
        self.is_spawned = True

        # When obj should be spawned
        now = datetime.now()
        self.spawn_timer = now + timedelta(seconds=random.randint(2, 5))

        # Where the portal is located
        x_pos = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        y_pos = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        self.position = (x_pos, y_pos)

        # TelePortal color = blue
        self.obj_color = (0, 0, 255)

        # teleportation portal Sprite images
        self.tele_portal_images = self.app.game.tele_portal_images

        # Entity's visual representation
        self.image = self.tele_portal_images[0]

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Interact sound
        self.sound_interact = self.app.game.sounds[2]
        self.sound_mod = 2.5
        effect_volume = app.app_config["settings"]["sound"]["effect_volume"]
        self.sound_interact_volume = float(effect_volume)/self.sound_mod

        # Active trigger
        self.activated = now

        # No Sight lines for tail segments
        self.sight_lines = []

        # Initilize starting children if it has no parent (and thus is the parent)
        if not parent:
            self.children.append(TelePortal(alpha_screen, screen, screen_size, app, parent=self))

        self.spawn()


    def update(self):
        # Verify if teleporter should be spawned
        now = datetime.now()
        if not self.is_spawned:
            pass
        elif now < self.spawn_timer:
            return False, False

        # teleporter is now spawned
        self.is_spawned = True

        # Set next spawn time
        self.spawn_timer = now + timedelta(seconds=random.randint(10, 25))

        # Mark previous position
        self.prev_position = self.position

        # try to spawn if obj can
        return self.spawn(), True


    def draw(self, updated_refresh, *kwargs):
        """
        draw


        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and (updated_refresh[0] or updated_refresh[1]):
            # print(self.position, self.prev_position, self.is_alive, self.children)

            # Render the teleportal based on it's parameters
            self.screen.blit(self.image, self.position)

            # Draw each child if there are any
            for child in self.children:
                child.draw(updated_refresh)


    def spawn(self):
        """
        spawn


        spawn does stuff
        """

        # Clear previous frame obj's location
        self.screen.fill((0, 0, 0, 0), (self.position[0], self.position[1], self.rect.width, self.rect.height))

        self.set_random_spawn()

        self.is_alive = True

        updated_child = False

        if self.children:
            for child in self.children:
                child.spawn()
            updated_child = True

        return True, updated_child


    def teleport(self, other_obj):
        """
        teleport


        teleport does stuff
        """

        # Is the child portal cuz has a parent
        if self.parent:
            # move other_obj to the parent portal
            other_obj.position = (self.parent.position[0], self.parent.position[1])
            self.parent.activated = datetime.now()

        # Is the parent portal cuz doesn't have a parent
        else:
            # move other_obj to the child portal
            other_obj.position = (self.children[0].position[0], self.children[0].position[1])
            self.children[0].activated = datetime.now()

        self.activated = datetime.now()


    def interact(self, interacting_obj):
        """
        interact


        interact does stuff
        """

        if self.activated + timedelta(seconds=self.abilty_cooldown) <= datetime.now():
            # teleport not on cooldown
            self.activated = datetime.now()

        else:
            # Teleport on cooldown
            return

        # Play second interacting_obj's interact sound
        sound = self.sound_interact
        effect_volume = self.app.app_config["settings"]["sound"]["effect_volume"]
        self.sound_interact_volume = float(effect_volume)/self.sound_mod
        sound.set_volume(self.sound_interact_volume)
        pygame.mixer.Sound.play(sound)

        # Teleport the obj to the paired portal
        self.teleport(interacting_obj)
