#!/usr/bin/env python3

"""
    Entity

    Base entity in the game

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from datetime import datetime
from gc import collect as gc_collect
from logging import warning as logging_warning
from random import randrange
from typing import Deque, TYPE_CHECKING
from uuid import uuid4

from faker import Faker
import pygame
from pygame import (
    BLEND_ADD,
    BLEND_RGBA_MULT,
    BLEND_RGBA_ADD,
    Color as pygame_Color,
    Surface,
    SRCALPHA,
    mixer,
    Rect,
    draw as pygame_draw,
)
from pygame.sprite import Sprite

from ..constants import (
    COLOR_BLACK,
    MENU_GAME_OVER,
    UP,
    RIGHT,
    DOWN,
    LEFT,
    UP_RIGHT,
    RIGHT_DOWN,
    DOWN_LEFT,
    LEFT_UP,
    WIDTH,
    HEIGHT,
    X,
    Y,
)

if TYPE_CHECKING:
    from ..game import Game


FAKE = Faker()


class Entity(Sprite):
    """Entity

    base obj for all entities
    """

    def __init__(self, game: "Game", screen_size: tuple[int, int], name: str):
        Sprite.__init__(self)

        # Base game obj
        self.game = game

        # Random name for this entity
        self.display_name = FAKE.first_name()

        # Unique identifier
        self.id = name + str(uuid4())

        # Entity is dead or alive
        self.is_alive = True

        # Determines if entity can be killed
        self.is_killable = True

        # Entity is a child/follower in a train of same children
        self.child_train = None

        # Entity ability cooldown timer
        self.abilty_cooldown = 1

        # Entity is player
        self.is_player = False

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
        self.size = self.game.grid_size

        # How fast the entity can move per loop-tick
        # 1 = 100%, 0 = 0%, speed can't be greater than 1
        self.speed_mod = 1
        self.base_speed = 30
        self.time_last_moved = datetime.now()

        # Where entity was looking = (Up = 0, Right = 1, Down = 2, Left = 3)
        self.prev_direction = DOWN
        self.child_prev_direction = DOWN

        # Default direction
        self.direction = DOWN

        # Determines how far the entity can see ahead of itself in the direction it's looking
        self.sight_mod = 2
        self.sight = self.sight_mod * self.size

        # RGB color = pink default
        self.obj_color = (255,105,180)

        # Entity's visual representation
        self.image = Surface((self.size, self.size))
        self.image.fill(self.obj_color)

        # Entity is a rectangle object
        self.rect = self.image.get_rect(topleft=self.position)

        # Default death sound
        if self.game.app.is_audio:
            self.sound_death = mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav")
            self.sound_mod = 4.5
            self.sound_death_volume = float(self.game.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod

        # Sight lines
        self.sight_lines = [
            Line(UP, self),
            Line(RIGHT, self),
            Line(DOWN, self),
            Line(LEFT, self),
        ]
        self.sight_lines_diag = [
            Line(UP_RIGHT, self),
            Line(RIGHT_DOWN, self),
            Line(DOWN_LEFT, self),
            Line(LEFT_UP, self),
        ]

        # Pathfinding variable
        self.target = None
        self.secondary_target = None
        self.since_secondary_target = datetime.now()

        # children list
        self.children: Deque[Entity] = Deque()


    def update(self) -> tuple[bool, bool]:
        """update

        update does stuff
        """

        # try to choose a direction if entity can
        self.choose_direction()

        # Try to move if entity can
        updated = self.move()

        return updated, False


    def draw(self, updated_refresh: tuple[bool, bool]) -> None:
        """draw

        draw does stuff
        """

        # render if alive and moved
        if self.is_alive and self.position != self.prev_position:
            # place hitbox at position
            self.rect.topleft = self.position

            # Render the entity based on it's image and position
            self.game.screen.blit(self.image, self.position)

            # Render the entity's sight lines
            draw = Line.draw # eval func only once
            for line in self.sight_lines:
                draw(line, self)

            for line in self.sight_lines_diag:
                draw(line, self)

            # Draw each child if there are any
            for child in self.children:
                child.draw(updated_refresh)


    def refresh_draw(self) -> None:
        """refresh_draw

        refresh_draw does stuff
        """

        # render if alive
        if self.is_alive:
            # Clear screen where self was
            # self.game.screen.fill(COLOR_BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            # Render the entity based on it's parameters
            self.game.screen.blit(self.image, self.position)

            # Re-draw each child if there are any
            for child in self.children:
                child.refresh_draw()


    def interact(self, interacting_obj: "Entity") -> None:
        """interact

        interact does stuff
        """

        # Play interacting_obj death sound
        if self.game.app.is_audio:
            sound = interacting_obj.sound_death
            interacting_obj.sound_death_volume = float(self.game.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod
            sound.set_volume(interacting_obj.sound_death_volume)
            mixer.Sound.play(sound)

        # Loose the game if interacting_obj is the player
        if interacting_obj.is_player:
            self.game.menu.menu_option = MENU_GAME_OVER

        # Kill interacting_obj
        interacting_obj.die(f"collided with {self.id} and died")


    def die(self, death_reason: str) -> None:
        """die

        die does stuff
        """

        if self.is_killable:
            # print(f"{self.id} {death_reason}")

            # Play death sound
            if self.game.app.is_audio:
                sound = self.sound_death
                self.sound_death_volume = float(self.game.app.app_config["settings"]["sound"]["effect_volume"])/self.sound_mod
                sound.set_volume(self.sound_death_volume)
                mixer.Sound.play(sound)

            # Loose the game if self is the player
            if self.is_player:
                self.game.app.menu.menu_option = MENU_GAME_OVER

            # Kill self
            self.is_alive = False

            # "remove" the entity from the game
            if "snake" in self.name:
                self.game.screen.fill(COLOR_BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

                self.game.sprite_group.remove(self)

                self.sight_lines_diag = None

                self.sight_lines = None

                if self.children:
                    for child in self.children:
                        self.game.screen.fill(COLOR_BLACK, (child.rect.x, child.rect.y, child.rect.width, child.rect.height))
                        child.kill()
                    self.children = None

                self.kill()

            # Clear previous frame render (from menu)
            # self.game.screen.fill(COLOR_BLACK)

            # draw the object
            for obj in self.game.sprite_group:
                obj.draw((False, True))

            # Free unreferenced memory
            gc_collect()


    def collision_checks(self, updated: bool) -> None:
        """collision_checks

        collision_checks does stuff
        """

        # Collision check for all entities
        for obj in self.game.sprite_group.sprites():
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


    def check_edge_collision(self) -> bool:
        """check_edge_collision

        Check for self collision/interaction to the edge of the screen
        """

        # Collision check for edge of screen (Right)
        if self.position[X] > self.screen_size[WIDTH]:
            if self.is_killable:
                self.die("Right edge of screen")

            else:
                # Set new location
                self.position = (0, self.position[Y])

            return True

        # Collision check for edge of screen (Bottom)
        elif self.position[Y] > self.screen_size[HEIGHT]:
            if self.is_killable:
                self.die("Bottom edge of screen")

            else:
                # Set new location
                self.position = (self.position[X], self.game.game_bar_height)

            return True

        # Collision check for edge of screen (Left)
        elif self.position[X] < 0:
            if self.is_killable:
                self.die("Left edge of screen")

            else:
                # Set new location
                self.position = (self.screen_size[WIDTH] - self.size, self.position[Y])

            return True

        # Collision check for edge of screen (Top)
        elif self.position[Y] < self.game.game_bar_height:
            if self.is_killable:
                self.die("Top edge of screen")

            else:
                # Set new location
                self.position = (self.position[X], self.screen_size[HEIGHT])

            return True

        return False


    def check_obj_collision(self, obj: "Entity") -> bool:
        """check_obj_collision

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


    def check_child_collision(self, obj: "Entity") -> bool:
        """check_child_collision

        Check for self to other obj's child collision/interaction
        """

        # Collision check between self and other obj's child
        if obj.children:
            # print(f"{obj.id} has children {obj.children}")
            for child in obj.children:
                try:
                    if Rect.colliderect(self.rect, child.rect):
                        if self.secondary_target == child.position:
                            self.secondary_target = None

                        # print(f"----{self.id} Interacting with child 1 {child.id}-----")

                        child.interact(self)

                        return True
                except RuntimeError as e:
                    logging_warning(f"Error: {e}")
        return False


    def set_random_spawn(self) -> None:
        """set_random_spawn

        Check for a random spawn location and if it's taken already
        """

        # set pre loop variables
        found_spawn = False

        # pylint: enable=access-member-before-definition
        while not found_spawn:
            # print(self.screen_size[WIDTH], self.game.game_bar_height)
            # Where the entity is located
            pos_x = self.screen_size[WIDTH] - randrange(
                self.size * 5, self.screen_size[WIDTH] - self.size * 5, self.size
            )

            pos_y = self.screen_size[HEIGHT] - randrange(
                self.size * 5, self.screen_size[HEIGHT] - self.game.game_bar_height - self.size * 5, self.size
            )

            # Check if the chosen random spawn location is taken
            taken = False
            for obj in self.game.sprite_group:
                if obj != self: # don't check self
                    if (pos_x, pos_y) == obj.position:
                        taken = True
                        break

                    elif obj.children:
                        for child in obj.children:
                            if child != self: # don't check self
                                if (pos_x, pos_y) == child.position:
                                    taken = True

                                    break

                    if taken == True:
                        break

            if taken == True:
                continue

            found_spawn = True

        # change position
        self.position = (pos_x, pos_y)

        # place hitbox at position
        self.rect.topleft = self.position


    def spawn(self) -> bool:
        """spawn

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


    def up_score(self, score_obj: "Entity") -> None:
        """up_score

        up_score does stuff
        """

        # Increase the score
        if self.is_alive:
            self.score += score_obj.point_value
            self.game.entity_final_scores[self.id] = {
                "is_player": self.is_player,
                "name": self.name + self.display_name,
                "score": self.score
            }


    def tint(self, tint_color):
        """ adds tint_color onto surf.
        """

        surf = self.image.copy()
        surf.fill(tint_color[0:3], None, pygame.BLEND_RGBA_MULT )
        self.image = surf


class Line(Sprite):
    """Line

    Sight line for a cardinal direction for an entity
    """

    def __init__(self, direction: int, entity: Entity):
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
            chosen_screen = entity.game.alpha_screen

        else :
            chosen_screen = entity.screen

        self.rect = pygame_draw.line(
            chosen_screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )


    def draw(self, entity: Entity) -> None:
        """draw

        draw does stuff
        """

        # Choose the screen to draw to
        if self.opasity == 0:
            chosen_screen = entity.game.alpha_screen

        else :
            chosen_screen = entity.screen

        # Clear previous frame obj's location
        chosen_screen.fill(COLOR_BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

        # determine entity's sightline end point and draw it
        self.line_options.get(self.direction)(entity)

        # Draw the line representing the rect
        self.rect = pygame_draw.line(
            chosen_screen,
            self.color,
            entity.rect.center,
            self.end,
            1,
        )


    def draw_up(self, entity: Entity) -> None:
        self.end = entity.rect.center[0], entity.rect.center[1] - entity.sight


    def draw_up_right(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] + entity.sight/1.5, entity.rect.center[1] - entity.sight/1.5


    def draw_right(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] + entity.sight, entity.rect.center[1]


    def draw_down_right(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] + entity.sight/1.5, entity.rect.center[1] + entity.sight/1.5


    def draw_down(self, entity: Entity) -> None:
        self.end = entity.rect.center[0], entity.rect.center[1] + entity.sight


    def draw_down_left(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] - entity.sight/1.5, entity.rect.center[1] + entity.sight/1.5


    def draw_left(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] - entity.sight, entity.rect.center[1]


    def draw_up_left(self, entity: Entity) -> None:
        self.end = entity.rect.center[0] - entity.sight/1.5, entity.rect.center[1] - entity.sight/1.5
