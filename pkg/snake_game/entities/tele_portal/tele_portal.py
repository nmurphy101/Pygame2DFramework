#!/usr/bin/env python3

'''
    Teleport Portal
    ~~~~~~~~~~

    a portal that can connect to another portal elsewhere


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import random
from datetime import datetime, timedelta
import pygame
# pylint: disable=relative-beyond-top-level
from ..entity import Entity
# pylint: enable=relative-beyond-top-level


class TelePortal(Entity):
    '''
    TelePortal
    ~~~~~~~~~~

    Teleport portal that entities can use to go to a connected portal elsewhere
    '''
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
        # When obj should be spawned
        self.spawn_timer = datetime.now() #+ timedelta(seconds=random.randint(1, 5))
        # Where the portal is located
        x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        self.position = (x, y)
        # TelePortal color = blue
        self.obj_color = (0, 0, 255)
        # teleportation portal Sprite images
        self.tele_portal_images = self.app.game.tele_portal_images
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)
        # Interact sound
        self.sound_interact = self.app.game.sounds[2]
        self.sound_mod = 2.5
        self.sound_interact_volume = float(app.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        # Active trigger
        self.activated = datetime.now()
        # No Sight lines for tail segments
        self.sight_lines = []
        # Initilize starting children if it has no parent (and thus is the parent)
        if not parent:
            self.children.append(TelePortal(alpha_screen, screen, screen_size, app, parent=self))

    def update(self, obj_container):
        # if datetime.now() >= self.spawn_timer:
        # try to spawn if obj can
        updated = self.spawn(obj_container)
        # else:
            # updated = False
        return updated

    def draw(self, obj_container, updated_refresh):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        # render if alive
        if self.alive:
            # place hitbox at position
            self.rect.topleft = self.position
            # Choose the correct image
            self.image = self.tele_portal_images[0]
            # Render the tail segment based on it's parameters
            self.screen.blit(self.image, self.position)
            # Draw each child if there are any
            for child in self.children:
                child.draw(obj_container, updated_refresh)

    def teleport(self, obj):
        '''
        teleport
        ~~~~~~~~~~

        teleport does stuff
        '''
        # Is the child portal cuz has a parent
        if self.parent:
            # move obj to the parent portal
            obj.position = (self.parent.position[0], self.parent.position[1])
            self.parent.activated = datetime.now()
        # Is the parent portal cuz doesn't have a parent
        else:
            # move obj to the child portal
            obj.position = (self.children[0].position[0], self.children[0].position[1])
            self.children[0].activated = datetime.now()

        self.activated = datetime.now()

    def interact(self, obj):
        '''
        interact
        ~~~~~~~~~~

        interact does stuff
        '''
        if self.activated + timedelta(seconds=self.abilty_cooldown) <= datetime.now():
            # teleport not on cooldown
            self.activated = datetime.now()
        else:
            # Teleport on cooldown
            return

        # Play second obj's interact sound
        sound = self.sound_interact
        self.sound_interact_volume = float(self.app.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        sound.set_volume(self.sound_interact_volume)
        pygame.mixer.Sound.play(sound)

        # Teleport the obj to the paired portal
        self.teleport(obj)
