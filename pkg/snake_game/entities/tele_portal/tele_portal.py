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
    def __init__(self, alpha_screen, screen, screen_size, base_game, parent=None):
        self.name = "portal_"
        # Initilize parent init
        super().__init__(screen, alpha_screen, screen_size, self.name, base_game)
        # Determines if entity can be killed
        self.killable = False
        # Ability cooldown timer
        self.abilty_cooldown = 1
        # Parent obj (means self is a child of said parent)
        self.parent = parent
        # When obj should be spawned
        self.spawn_timer = datetime.now() #+ timedelta(seconds=random.randint(1, 5))
        # Where the portal is located
        self.pos_x = self.screen_size[0] - random.randrange(
            16, self.screen_size[0], 16
        )
        self.pos_y = self.screen_size[1] - random.randrange(
            16, self.screen_size[1], 16
        )
        # TelePortal color = blue
        self.obj_color = (0, 0, 255)
        # Interact sound
        self.sound_interact = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/SciFi05.wav")
        self.sound_interact_volume = float(base_game.game.game_config["settings"]["effect_volume"])/1.5
        # Active trigger
        self.activated = datetime.now()
        # Initilize starting children if it has no parent (and thus is the parent)
        if not parent:
            self.children.append(TelePortal(alpha_screen, screen, screen_size, base_game, parent=self))

    def spawn(self, obj_dict):
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
                self.pos_x = self.screen_size[0] - random.randrange(
                    self.size*5, self.screen_size[0] - self.size * 5, self.size
                )
                self.pos_y = self.screen_size[1] - random.randrange(
                    self.size*5, self.screen_size[1] - self.size * 5, self.size
                )

                # Check if the chosen random spawn location is taken
                for _, oth_obj in obj_dict.items():
                    collision_bool = self.rect.collidepoint(self.pos_x, self.pos_y)

                    if collision_bool:
                        break

                if collision_bool:
                    continue

                for _, oth_obj in obj_dict.items():
                    try:
                        if oth_obj.children:
                            self.rect.collidelist(oth_obj.children)
                    except AttributeError:
                        pass

                found_spawn = True

            self.alive = True

        if self.children:
            for child in self.children:
                child.spawn(obj_dict)


    def teleport(self, oth_obj):
        '''
        teleport
        ~~~~~~~~~~

        teleport does stuff
        '''
        # Is the parent portal
        if self.parent is None:
            # move obj to the child portal
            oth_obj.pos_x = self.children[0].pos_x
            oth_obj.pos_y = self.children[0].pos_y
            self.children[0].activated = datetime.now()
        # Is the child portal
        else:
            # move obj to the parent portal
            oth_obj.pos_x = self.parent.pos_x
            oth_obj.pos_y = self.parent.pos_y
            self.parent.activated = datetime.now()

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
            if obj1.rect.colliderect(child):
                child.interact(obj1)
