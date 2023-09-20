#!/usr/bin/env python3

"""
    Entity

    Base entity in the game

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import random
import math
from datetime import datetime
from typing import Deque
import uuid

from faker import Faker
import pygame
from pygame.sprite import Sprite



FAKE = Faker()


class Entity(Sprite):
    """Entity

    base obj for all entities
    """

    def __init__(self, alpha_screen, screen, screen_size, name, app):
        pygame.sprite.Sprite.__init__(self)

        # Base game obj
        self.app = app

        # Random name for this entity
        self.display_name = FAKE.first_name()

        # Unique identifier
        self.id = name + str(uuid.uuid4())

        # Entity is dead or alive
        self.is_alive = True

        # Determines if entity can be killed
        self.killable = True

        # Entity is a child/follower in a train of same children
        self.child_train = None

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

        # Where the entity was located
        self.prev_position = None

        # How big entity is
        self.size = 16

        # How fast the entity can move per loop-tick
        # 1 = 100%, 0 = 0%, speed can't be greater than 1
        self.speed_mod = 1
        self.base_speed = 30
        self.time_last_moved = datetime.now()

        # Where entity was looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.prev_direction = 2
        self.child_prev_direction = 2

        # Where entity is looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.direction = 2

        # Determines how far the entity can see ahead of itself in the direction it's looking
        self.sight_mod = 2
        self.sight = self.sight_mod * self.size

        # Obj pos/size  = (left, top, width, height)
        # self.obj = (self.position[0], self.position[1], self.size+8, self.size)
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
        self.sound_death_volume = float(self.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        # Sight lines
        self.sight_lines = [
            Line(0, self),
            Line(1, self),
            Line(2, self),
            Line(3, self),
        ]
        self.sight_lines_diag = [
            Line(.5, self),
            Line(1.5, self),
            Line(2.5, self),
            Line(3.5, self),
        ]

        # Pathfinding variable
        self.target = None
        self.secondary_target = None
        self.since_secondary_target = datetime.now()
        self.ai_difficulty = 10

        # children list
        self.children = Deque()


    def update(self):
        """
        update

        update does stuff
        """

        # try to choose a direction if entity can
        self.choose_direction()

        # Try to move if entity can
        updated = self.move()

        # Return if this entity updated since last tick
        return updated, False


    def draw(self, updated_refresh):
        """
        draw


        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and self.position != self.prev_position:
            # place hitbox at position
            self.rect.topleft = self.position

            # Render the tail segment based on it's parameters
            self.screen.blit(self.image, self.position)

            # Render the entity's sight lines
            draw = Line.draw # eval func only once
            for line in self.sight_lines:
                draw(line, self)

            for line in self.sight_lines_diag:
                draw(line, self)

            # Draw each child if there are any
            for child in self.children:
                child.draw(updated_refresh)


    def refresh_draw(self):
        """
        refresh_draw


        refresh_draw does stuff
        """

        # render if alive
        if self.is_alive:
            # Clear screen where self was
            # self.screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            # Render the entity based on it's parameters
            self.screen.blit(self.image, self.position)

            # Re-draw each child if there are any
            for child in self.children:
                child.refresh_draw()


    def interact(self, interacting_obj):
        """
        interact


        interact does stuff
        """

        # Play interacting_obj death sound
        sound = interacting_obj.sound_death
        interacting_obj.sound_death_volume = float(self.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod
        sound.set_volume(interacting_obj.sound_death_volume)
        pygame.mixer.Sound.play(sound)

        # Loose the game if interacting_obj is the player
        if interacting_obj.player:
            self.app.game.menu.menu_option = 3

        # Kill interacting_obj
        interacting_obj.die(f"collided with {self.id} and died")


    def die(self, death_reason):
        if self.killable:
            # print(f"{self.id} {death_reason}")

            # Play death sound
            sound = self.sound_death
            self.sound_death_volume = float(self.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod
            sound.set_volume(self.sound_death_volume)
            pygame.mixer.Sound.play(sound)

            # Loose the game if self is the player
            if self.player:
                self.app.game.menu.menu_option = 3

            # Kill self
            self.is_alive = False

            # "remove" the entity from the game
            if "snake" in self.name:
                self.app.game.entity_final_scores[self.id] = {
                    "is_player": self.player,
                    "name": self.name + self.display_name,
                    "score": self.score
                }
                self.screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

                self.app.game.sprite_group.remove(self)

            # Clear previous frame render (from menu)
            self.app.game.screen.fill((0, 0, 0, 0))

            # draw the object
            for obj in self.app.game.sprite_group:
                obj.draw((False, True))


    def collision_checks(self, updated):
        """
        collision_checks


        collision_checks does stuff
        """

        # Collision check for all entities
        for obj in self.app.game.sprite_group.sprites():
            # Make sure not checking collision with dead obj's
            if not self.is_alive or not obj.is_alive:
                continue

            collision = False

            # Allow for early termination of checks
            while not collision:
                # Make sure not checking collision with self
                if self != obj and updated:
                    # Collision check between self and other obj
                    collision = self.check_obj_collision(obj)

                    # Screen edge collision check
                    collision = self.check_edge_collision()

                # Collision check between self and obj's children even if self=obj
                collision = self.check_child_collision(obj)

                # Always exit the while loop at the end
                collision = True


    def check_edge_collision(self):
        """
        check_edge_collision


        Check for self collision/interaction to the edge of the screen
        """

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
        """
        check_obj_collision


        Check for self to other obj collision/interaction
        """

        # Collision check between self and other obj
        if self.rect.colliderect(obj):
            if self.secondary_target == obj.position:
                self.secondary_target = None

            # print(self.id, " Interacting with obj ", obj.id)

            # Do obj's interaction method
            obj.interact(self)

            return True

        return False


    def check_child_collision(self, obj):
        """
        check_child_collision


        Check for self to other obj's child collision/interaction
        """

        # Collision check between self and other obj's child
        if obj.children:
            # print(f"{obj.id} has children {obj.children}")
            for child in obj.children:
                if pygame.Rect.colliderect(self.rect, child.rect):
                    if self.secondary_target == child.position:
                        self.secondary_target = None

                    # print(f"----{self.id} Interacting with child 1 {child.id}-----")
                    # print(f"child pos: {child.tail_pos}/{len(obj.children)}")

                    child.interact(self)

                    return True

        return False


    def set_random_spawn(self):
        """
        set_random_spawn


        Check for a random spawn location and if it's taken already
        """

        # set pre loop variables
        found_spawn = False

        # pylint: enable=access-member-before-definition
        while not found_spawn:
            # Where the entity is located
            x = self.screen_size[0] - random.randrange(
                self.size*5, self.screen_size[0] - self.size * 5, self.size
            )

            y = self.screen_size[1] - random.randrange(
                self.size*5, self.screen_size[1] - self.size * 5, self.size
            )

            # Check if the chosen random spawn location is taken
            taken = False
            for obj in self.app.game.sprite_group:
                if obj != self: # don't check self
                    if (x, y) == obj.position:
                        taken = True
                        break

                    elif obj.children:
                        for child in obj.children:
                            if child != self: # don't check self
                                if (x, y) == child.position:
                                    taken = True

                                    break

                    if taken == True:
                        break

            if taken == True:
                continue

            found_spawn = True

        # change position
        self.position = (x, y)

        # place hitbox at position
        self.rect.topleft = self.position


    def aquire_primary_target(self, target_name):
        # Set variables pre loop
        primary_target = (None, 10000*100000)

        pos = (self.app.game.screen_size[0]/2, self.app.game.screen_size[1]/2)

        for obj in self.app.game.sprite_group.sprites():
            if target_name in obj.id:
                dist_self = math.hypot(obj.position[0] - self.position[0], obj.position[1] - self.position[1])
                if dist_self < primary_target[1]:
                    pos = (obj.position[0], obj.position[1])
                    primary_target = (pos, dist_self)

        self.target = (target_name, primary_target[0][0], primary_target[0][1])

        self.direction = self.app.game.chosen_ai.decide_direction(
            self,
            self.target,
            difficulty=self.ai_difficulty,
        )

        self.since_secondary_target = datetime.now()


    def spawn(self):
        """
        spawn


        spawn does stuff
        """

        if not self.is_alive:
            # Mark previous position
            self.prev_position = self.position

            self.set_random_spawn()

            self.is_alive = True

            if self.children:
                for child in self.children:
                    child.spawn()

            return True

        return False


    def choose_img(self):
        pass


    def grow(self, eaten_obj):
        pass


    def up_score(self, score_obj):
        """
        up_score


        up_score does stuff
        """

        # Increase the score
        if self.is_alive:
            self.score += score_obj.point_value


    def choose_direction(self):
        pass


    def move(self):
        return None


    def teleport(self, other_obj):
        pass


class Line(Sprite):
    """Line

    Sight line for a cardinal direction for an entity
    """

    def __init__(self, direction, entity):
        self.open = True
        self.opasity = 0 # Change this to 1 if you want to see sightlines
        self.color = (255, 105, 180, (self.opasity))
        self.direction = direction

        # determine entity's sightline end point
        self.line_options = {
            0: lambda *args: self.draw_up(*args),
            .5: lambda *args: self.draw_up_right(*args),
            1: lambda *args: self.draw_right(*args),
            1.5: lambda *args: self.draw_down_right(*args),
            2: lambda *args: self.draw_down(*args),
            2.5: lambda *args: self.draw_down_left(*args),
            3: lambda *args: self.draw_left(*args),
            3.5: lambda *args: self.draw_up_left(*args),
        }

        self.line_options.get(self.direction)(entity)

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
        """
        draw


        draw does stuff
        """

        # Choose the screen to draw to
        if self.opasity == 0:
            chosen_screen = entity.alpha_screen

        else :
            chosen_screen = entity.screen

        # Clear previous frame obj's location
        chosen_screen.fill((0, 0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

        # determine entity's sightline end point and draw it
        self.line_options.get(self.direction)(entity)

        # Draw the line representing the rect
        self.rect = pygame.draw.line(
            chosen_screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )


    def draw_up(self, entity):
        self.end = entity.rect.center[0], entity.rect.center[1] - entity.sight


    def draw_up_right(self, entity):
        self.end = entity.rect.center[0] + entity.sight/1.5, entity.rect.center[1] - entity.sight/1.5


    def draw_right(self, entity):
        self.end = entity.rect.center[0] + entity.sight, entity.rect.center[1]


    def draw_down_right(self, entity):
        self.end = entity.rect.center[0] + entity.sight/1.5, entity.rect.center[1] + entity.sight/1.5


    def draw_down(self, entity):
        self.end = entity.rect.center[0], entity.rect.center[1] + entity.sight


    def draw_down_left(self, entity):
        self.end = entity.rect.center[0] - entity.sight/1.5, entity.rect.center[1] + entity.sight/1.5


    def draw_left(self, entity):
        self.end = entity.rect.center[0] - entity.sight, entity.rect.center[1]


    def draw_up_left(self, entity):
        self.end = entity.rect.center[0] - entity.sight/1.5, entity.rect.center[1] - entity.sight/1.5
