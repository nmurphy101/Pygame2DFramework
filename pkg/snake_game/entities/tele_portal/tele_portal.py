#!/usr/bin/env python3

'''
    Teleport Portal
    ~~~~~~~~~~

    a portal that can connect to another portal elsewhere


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

from datetime import datetime, timedelta
import random
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
        self.name = "TelePortal_"
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
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)
        # Interact sound
        self.sound_interact = self.app.game.sounds[2]
        self.sound_mod = 2.5
        self.sound_interact_volume = float(app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        # Active trigger
        self.activated = datetime.now()
        # No Sight lines for tail segments
        self.sight_lines = []
        # Initilize starting children if it has no parent (and thus is the parent)
        if not parent:
            self.children.append(TelePortal(alpha_screen, screen, screen_size, app, parent=self))

    def spawn(self, obj_container):
        '''
        spawn
        ~~~~~~~~~~

        spawn does stuff
        '''
        found_spawn = False
        # pylint: disable=access-member-before-definition
        if not self.alive and datetime.now() > self.spawn_timer:
            # pylint: enable=access-member-before-definition
            while not found_spawn:
                # Where the portal is located
                x = self.screen_size[0] - random.randrange(
                    self.size*5, self.screen_size[0] - self.size * 5, self.size
                )
                y = self.screen_size[1] - random.randrange(
                    self.size*5, self.screen_size[1] - self.size * 5, self.size
                )
                self.position = (x, y)

                # Check if the chosen random spawn location is taken
                for oth_obj in obj_container:
                    collision_bool = self.rect.collidepoint(self.position[0], self.position[1])

                    if collision_bool:
                        break

                if collision_bool:
                    continue

                for oth_obj in obj_container:
                    try:
                        if oth_obj.children:
                            self.rect.collidelist(oth_obj.children)
                    except AttributeError:
                        pass

                found_spawn = True

            self.alive = True

        if self.children:
            for child in self.children:
                child.spawn(obj_container)


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

    def interact(self, obj1):
        '''
        interact
        ~~~~~~~~~~

        interact does stuff
        '''
        if self.activated + timedelta(seconds=self.abilty_cooldown) < datetime.now():
            # teleport not on cooldown
            self.activated = datetime.now()
        else:
            # Teleport on cooldown
            return

        # Play second obj's interact sound
        sound = self.sound_interact
        self.sound_interact_volume = float(self.app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        sound.set_volume(self.sound_interact_volume)
        pygame.mixer.Sound.play(sound)

        # Teleport the obj to the paired portal
        self.teleport(obj1)

    def interact_children(self, obj1):
        '''
        interact_children
        ~~~~~~~~~~

        interact_children does stuff
        '''
        for child in self.children:
            if pygame.sprite.collide_rect(obj1, child):
                child.interact(obj1)
