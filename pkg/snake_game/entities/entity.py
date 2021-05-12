#!/usr/bin/env python3

'''
    Entitie
    ~~~~~~~~~~

    Base entity in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import uuid
import pygame


class Entity():
    '''
    Entity
    ~~~~~~~~~~

    base obj for all entities
    '''
    def __init__(self, alpha_screen, screen, screen_size, name, app):
        # Base game obj
        self.app = app
        # Unique identifier
        self.ID = name + str(uuid.uuid4())
        # Entity is dead or alive
        self.alive = False
        # Determines if entity can be killed
        self.killable = True
        # Entity ability cooldown timer
        self.abilty_cooldown = 1
        # Entity is player
        self.player = False
        # Screen obj
        self.alpha_screen = alpha_screen
        self.screen = screen
        # Score this entity has accumulated
        self.score = 0
        # Where the entity was located
        self.prev_pos_x = -20
        self.prev_pos_y = -20
        # Size of the game screen
        self.screen_size = screen_size
        # Where the entity is located
        self.pos_x = -20
        self.pos_y = -20
        # How big entity is
        self.size = 16
        # How fast the entity can move per loop-tick
        # 1 = 100%, 0 = 0%, speed can't be greater than 1
        self.speed = 1
        self.moved_last_cnt = 0
        # Where entity was looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.prev_direction = 2
        # Where entity is looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.direction = 2
        # Determines how far the entity can see ahead of itself in the direction it's looking
        self.sight = 2 * self.size
        # Obj pos/size  = (left, top, width, height)
        self.obj = (self.pos_x, self.pos_y, self.size+8, self.size)
        self.death_obj = (-10000*10000, -10000*10000, 0, 0)
        # RGB color = pink default
        self.obj_color = (255,105,180)
        # Entity is a rectangle object
        self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)
        # Default death sound
        self.sound_death = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav")
        self.sound_mod = 4.5
        self.sound_death_volume = float(app.game.game_config["settings"]["effect_volume"])/self.sound_mod
        # Sight lines
        self.sight_lines = [
            Line(0, self),
            Line(2, self),
            Line(3, self),
            Line(1, self),
        ]
        # Pathfinding variables
        self.target = None
        self.secondary_target = None
        # children list
        self.children = []

    def draw(self, screen, obj_dict):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Draw each child if there are any
            if self.children:
                for child in self.children:
                    child.draw(screen, obj_dict)
            # obj pos/size  = (left, top, width, height)
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the entity's obj based on it's parameters
            self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)
            # Render the entity's sight lines
            for line in self.sight_lines:
                line.draw(self)

    def interact(self, obj1):
        pass

    def interact_children(self, obj1):
        i = 0
        if self.children:
            for child in self.children:
                if child.alive:
                    if obj1.rect.colliderect(child):
                        if obj1.killable:
                            print("Child collision")
                            # Play obj1 death sound
                            sound = obj1.sound_death
                            self.sound_death_volume = float(self.app.game.game_config["settings"]["effect_volume"])/self.sound_mod
                            sound.set_volume(obj1.sound_death_volume)
                            pygame.mixer.Sound.play(sound)
                            # Loose the game if obj1 is the player
                            if obj1.player:
                                self.app.game.menu.menu_option = 3
                            # Kill obj1
                            obj1.alive = False

    def die(self, death_reason):
        if self.killable:
            # print(f"{self.ID} {death_reason}")
            # Play death sound
            sound = self.sound_death
            self.sound_death_volume = float(self.app.game.game_config["settings"]["effect_volume"])/self.sound_mod
            sound.set_volume(self.sound_death_volume)
            pygame.mixer.Sound.play(sound)
            # Loose the game if self is the player
            if self.player:
                self.app.game.menu.menu_option = 3
            # Kill self
            self.alive = False
            self.rect = pygame.draw.rect(self.screen, self.obj_color, self.death_obj)
            if self.children:
                for child in self.children:
                    child.alive = False
                    child.rect = pygame.draw.rect(self.screen, self.obj_color, self.death_obj)

    def get_speed(self, entity_speed):
        real_speed = entity_speed * (self.app.logic_fps/int(self.app.clock.get_fps()))
        return real_speed

    def grow(self, eaten_obj):
        pass

    def up_score(self, eaten_obj):
        pass

    def move(self):
        pass

    def aquire_primary_target(self, target_name):
        pass

    def spawn(self, obj_dict):
        pass

    def teleport(self, oth_obj):
        pass


class Line():
    '''
    Line
    ~~~~~~~~~~

    Sight line for a cardinal direction for an entity
    '''
    def __init__(self, direction, entity):
        self.open = True
        self.opasity = 0 # Change this to 1 if you want to see sightlines
        self.color = (255, 105, 180, (self.opasity))
        self.direction = direction
        if direction == 0:
            self.end = entity.rect.center[0], entity.rect.center[1] - entity.sight
        elif direction == 2:
            self.end = entity.rect.center[0], entity.rect.center[1] + entity.sight
        elif direction == 3:
            self.end = entity.rect.center[0] - entity.sight, entity.rect.center[1]
        elif direction == 1:
            self.end = entity.rect.center[0] + entity.sight, entity.rect.center[1]
        self.rect = pygame.draw.line(
            entity.screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )

    def draw(self, entity):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        # determine entity's sightline end point
        if self.direction == 0:
            self.end = entity.rect.center[0], entity.rect.center[1] - entity.sight
        elif self.direction == 2:
            self.end = entity.rect.center[0], entity.rect.center[1] + entity.sight
        elif self.direction == 3:
            self.end = entity.rect.center[0] - entity.sight, entity.rect.center[1]
        elif self.direction == 1:
            self.end = entity.rect.center[0] + entity.sight, entity.rect.center[1]
        # Render the entity's sight line
        self.rect = pygame.draw.line(
            entity.screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )
