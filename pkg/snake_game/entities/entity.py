#!/usr/bin/env python3

'''
    Entitie
    ~~~~~~~~~~

    Base entity in the game


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import random
import math
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
        pygame.sprite.Sprite.__init__(self)
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
        self.prev_position = (-20, -20)
        # Size of the game screen
        self.screen_size = screen_size
        # Where the entity is located
        self.position = (-20, -20)
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
        self.obj = (self.position[0], self.position[1], self.size+8, self.size)
        self.death_position = (-10000*10000, -10000*10000)
        # RGB color = pink default
        self.obj_color = (255,105,180)
        # Entity's visual representation
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.obj_color)
        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)
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
            # obj pos/size  = (left, top, width, height)
            self.obj = (self.position[0], self.position[1], self.size, self.size)
            # Render the entity's obj based on it's parameters
            self.rect.topleft = self.position
            screen.blit(self.image, self.position)
            # Render the entity's sight lines
            for line in self.sight_lines:
                line.draw(self)
            # Draw each child if there are any
            if self.children:
                for child in self.children:
                    child.draw(screen, obj_container)

    def interact(self, interacting_obj):
        # Play interacting_obj death sound
        sound = interacting_obj.sound_death
        interacting_obj.sound_death_volume = float(self.app.game.game_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        sound.set_volume(interacting_obj.sound_death_volume)
        pygame.mixer.Sound.play(sound)
        # Loose the game if interacting_obj is the player
        if interacting_obj.player:
            self.app.game.menu.menu_option = 3
        # Kill interacting_obj
        interacting_obj.die(f"collided with {self.ID} and died")

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
            self.position = self.death_position
            self.rect.topleft = self.position
            if self.children:
                for child in self.children:
                    child.alive = False
                    child.position = self.death_position
                    child.rect.topleft = child.position

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
                collision = False
                while not collision: # Allow for early termination of checks
                    # Make sure not checking collision with self
                    if self != obj:
                        # Collision check between self and other obj
                        collision = self.check_obj_collision(obj)
                        # Screen edge collision check
                        collision = self.check_edge_collision()
                    # Collision check between self and obj's children even if self=obj
                    collision = self.check_child_collision(obj)
                    # Always exit the while loop at the end
                    collision = True

    def check_edge_collision(self):
        '''
        check_edge_collision
        ~~~~~~~~~~

        Check for self collision/interaction to the edge of the screen
        '''
        # Collision check for edge of screen (Right and Bottom)
        if (self.position[0] > self.screen_size[0]-self.size) or (
                self.position[1] > self.screen_size[1]-self.size):
            self.die("Edge of screen")
            return True
        # Collision check for edge of screen (Left and Top)
        elif self.position[0] < 0 or self.position[1] < 0:
            self.die("Edge of screen")
            return True
        return False

    def check_obj_collision(self, obj):
        '''
        check_obj_collision
        ~~~~~~~~~~

        Check for self to other obj collision/interaction
        '''
        # Collision check between self and other obj
        if pygame.sprite.collide_rect(self, obj):
            if self.secondary_target == obj.position:
                self.secondary_target = None
            # print(self.ID, " Interacting with obj ", obj.ID)
            # Do obj's interaction method
            obj.interact(self)
            return True


        return False

    def check_child_collision(self, obj):
        '''
        check_child_collision
        ~~~~~~~~~~

        Check for self to other obj's child collision/interaction
        '''
        # Collision check between self and other obj's child
        if obj.children:
            # print(f"{obj.ID} has children {obj.children}")
            for child in obj.children:
                if pygame.sprite.collide_rect(self, child):
                    if self.secondary_target == child.position:
                        self.secondary_target = None
                    # print(f"----{self.ID} Interacting with child 1 {child.ID}-----")
                    # print(f"child pos: {child.tail_pos}/{len(obj.children)}")
                    child.interact(self)
                    return True
        return False

    def set_random_spawn(self, obj_container):
        '''
        set_random_spawn
        ~~~~~~~~~~

        Check for a random spawn location and if it's taken already
        '''
        found_spawn = False
        # pylint: enable=access-member-before-definition
        while not found_spawn:
            # Where the food is located
            x = self.screen_size[0] - random.randrange(
                self.size*5, self.screen_size[0] - self.size * 5, self.size
            )
            y = self.screen_size[1] - random.randrange(
                self.size*5, self.screen_size[1] - self.size * 5, self.size
            )
            self.position = (x, y)

            # Check if the chosen random spawn location is taken
            taken = False
            for obj in obj_container:
                if obj != self: # don't check self
                    if self.position == obj.position:
                        taken = True
                        break
                    elif obj.children:
                        for child in obj.children:
                            if self.position == child.position:
                                taken = True
                                break
                    if taken == True:
                        break
            if taken == True:
                continue
            self.rect = self.image.get_rect(topleft=self.position)
            found_spawn = True

    def aquire_primary_target(self, target_name):
        primary_target = (None, 10000*100000)
        for obj in self.app.game.obj_container:
            if target_name in obj.ID:
                dist_self = math.hypot(obj.position[0] - self.position[0], obj.position[1] - self.position[1])
                if dist_self < primary_target[1]:
                    primary_target = (obj, dist_self)
        self.target = (primary_target[0].position[0], primary_target[0].position[1])
        self.direction = self.app.game.chosen_ai.decide_direction(
            self, self.target, self.app.game.obj_container, difficulty=0
        )

    def grow(self, eaten_obj):
        pass

    def up_score(self, eaten_obj):
        pass

    def choose_direction(self):
        pass

    def move(self):
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
        if self.opasity == 0:
            chosen_screen = entity.alpha_screen
        else :
            chosen_screen = entity.screen
        self.rect = pygame.draw.line(
            chosen_screen,
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
        if self.opasity == 0:
            chosen_screen = entity.alpha_screen
        else :
            chosen_screen = entity.screen
        self.rect = pygame.draw.line(
            chosen_screen,
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
