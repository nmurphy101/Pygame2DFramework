#!/usr/bin/env python3

'''
    Entitie
    ~~~~~~~~~~

    Base entity in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

from datetime import datetime
import uuid
import pygame
from pygame.sprite import Sprite

class Entity(Sprite):
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
        self.movement = 1
        self.base_speed = 30
        self.time_last_moved = datetime.now()
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
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        # Default death sound
        self.sound_death = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav")
        self.sound_mod = 4.5
        self.sound_death_volume = float(app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
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

    def draw(self, screen, obj_container):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Draw each child if there are any
            if self.children:
                for child in self.children:
                    child.draw(screen, obj_container)
            # obj pos/size  = (left, top, width, height)
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the entity's obj based on it's parameters
            self.rect.topleft = (self.pos_x, self.pos_y)
            screen.blit(self.image, self.position)
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
                            self.sound_death_volume = float(self.app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
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
            self.sound_death_volume = float(self.app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
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

    def collision_checks(self):
        '''
        collision_checks
        ~~~~~~~~~~

        collision_checks does stuff
        '''
        # Collision check for all entities
        for obj in self.app.game.obj_container:
            # Make sure not checking collision with dead obj's
            if self.alive and obj.alive:
                # Make sure not checking collision with self
                if self != obj:
                    # Collision check between obj and other obj
                    self.check_obj_to_obj_collision(obj)
                    # Screen edge collision check
                    self.check_edge_collision()
                # Collision check between self and obj's children even if self=obj
                obj.interact_children(self)

    def check_edge_collision(self):
        '''
        check_edge_collision
        ~~~~~~~~~~

        Check for self collision/interaction to the edge of the screen
        '''
        # Collision check for edge of screen (Right and Bottom)
        if (self.pos_x > self.screen_size[0]-self.size) or (
                self.pos_y > self.screen_size[1]-self.size):
            self.die("Edge of screen")
        # Collision check for edge of screen (Left and Top)
        elif self.pos_x < 0 or self.pos_y < 0:
            self.die("Edge of screen")

    def check_obj_to_obj_collision(self, obj2):
        '''
        check_obj_to_obj_collision
        ~~~~~~~~~~

        Check for obj1 to obj2 collision/interaction
        '''
        # Collision check between obj1 and other obj2
        if self.rect.colliderect(obj2):
            if self.secondary_target:
                self.secondary_target = None

            # print(self, " Interacting with ", obj2)
            # Do obj2's interaction method
            obj2.interact(self)

    def grow(self, eaten_obj):
        pass

    def up_score(self, eaten_obj):
        pass

    def choose_direction(self):
        pass

    def move(self):
        pass

    def aquire_primary_target(self, target_name):
        pass

    def spawn(self, obj_container):
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
        # determine entity's sightline end point
        draw_line = {
            0: lambda: self.draw_up(entity),
            2: lambda: self.draw_down(entity),
            3: lambda: self.draw_left(entity),
            1: lambda: self.draw_right(entity),
        }.get(self.direction)
        # Run the chosen line to draw
        draw_line()
        self.rect = pygame.draw.line(
            entity.alpha_screen,
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
        draw_line = {
            0: lambda: self.draw_up(entity),
            2: lambda: self.draw_down(entity),
            3: lambda: self.draw_left(entity),
            1: lambda: self.draw_right(entity),
        }.get(self.direction)
        # Run the chosen line to draw
        draw_line()
        # Draw the line representing the rect
        self.rect = pygame.draw.line(
            entity.alpha_screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )

    def draw_up(self, entity):
        self.end = entity.rect.center[0], entity.rect.center[1] - entity.sight

    def draw_down(self, entity):
        self.end = entity.rect.center[0], entity.rect.center[1] + entity.sight

    def draw_left(self, entity):
        self.end = entity.rect.center[0] - entity.sight, entity.rect.center[1]

    def draw_right(self, entity):
        self.end = entity.rect.center[0] + entity.sight, entity.rect.center[1]
