#!/usr/bin/env python3

'''
    Snake
    ~~~~~~~~~~

    It's a snake


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame
# pylint: disable=no-name-in-module
from pygame.constants import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)
# pylint: enable=no-name-in-module
# pylint: disable=relative-beyond-top-level
from ..entity import Entity
from ...ai.a_star import a_star_search, reconstruct_path
# pylint: enable=relative-beyond-top-level

SNAKE_DEATH = 0


class Snake(Entity):
    '''
    Snake
    ~~~~~~~~~~

    obj for the snake
    '''
    def __init__(self, screen, screen_size, base_game):
        # Name for this type of object
        self.name = "snake_"
        # Initilize parent init
        super().__init__(screen, screen_size, self.name, base_game)
        # Default set snake to alive
        self.alive = True
        # Snake is player
        self.player = True
        # Where the snake was located
        self.prev_pos_x = 96
        self.prev_pos_y = 96
        # Where the snake is started located
        self.pos_x = 96
        self.pos_y = 112
        # How big snake parts are
        self.size = 16
        # How fast the snake can move per loop-tick
        # 1 = 100%, 0 = 0%, speed can't be greater than 1
        self.speed = .75
        # head color = red
        self.obj_color = (255, 0, 0)
        # Snake death sound
        self.sound_death = pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav")
        self.sound_death_volume = base_game.effect_volume/4.5
        # Interact sound
        # self.sound_interact = pygame.mixer.Sound("")
        # Number of tail segments
        self.num_tails = 5
        # Initilize starting tails
        for pos in range(self.num_tails+1):
            if pos == 0:
                self.children.append(TailSegment(screen, screen_size, base_game, self, pos))
            else:
                self.children.append(TailSegment(screen, screen_size, base_game, self.children[pos-1], pos))

    def grow(self, eaten_obj):
        '''
        grow
        ~~~~~~~~~~

        grow does stuff
        '''
        # Add a new tail segment
        if self.alive:
            for _ in range(eaten_obj.growth):
                self.children.append(TailSegment(
                    self.screen,
                    self.screen_size,
                    self.base_game,
                    self.children[self.num_tails - 1],
                    self.num_tails + 1
                ))
                self.num_tails += 1

    def up_score(self, eaten_obj):
        '''
        up_score
        ~~~~~~~~~~

        up_score does stuff
        '''
        # Increase the score
        if self.alive:
            # pylint: disable=no-member
            self.score += eaten_obj.point_value
            # pylint: enable=no-member

    def choose_direction(self):
        '''
        choose_direction
        ~~~~~~~~~~

        choose_direction does stuff
        ''''
        if self.player:
            key = pygame.key.get_pressed()
            # pylint: disable=access-member-before-definition
            if key[K_UP] and self.direction != 0 and self.prev_direction != 2:
                # pylint: disable=access-member-before-definition
                self.direction = 0
            elif key[K_DOWN] and self.direction != 2 and self.prev_direction != 0:
                self.direction = 2
            elif key[K_LEFT] and self.direction != 3 and self.prev_direction != 1:
                self.direction = 3
            elif key[K_RIGHT] and self.direction != 1 and self.prev_direction != 3:
                self.direction = 1
        else:
            pass

    def move(self):
        '''
        move
        ~~~~~~~~~~

        move does stuff
        '''
        if self.player:
            # pylint: disable=access-member-before-definition
            if self.moved_last_cnt >= 1 and self.alive:
                # pylint: disable=access-member-before-definition
                # Save current position as last position
                self.prev_pos_x = self.pos_x
                self.prev_pos_y = self.pos_y
                # Moving up
                if self.direction == 0:
                    self.prev_direction = self.direction
                    self.pos_y -= self.size
                # Moving down
                elif self.direction == 2:
                    self.prev_direction = self.direction
                    self.pos_y += self.size
                # Moving left
                elif self.direction == 3:
                    self.prev_direction = self.direction
                    self.pos_x -= self.size
                # Moving right
                elif self.direction == 1:
                    self.prev_direction = self.direction
                    self.pos_x += self.size
                self.moved_last_cnt = 0
            else:
                self.moved_last_cnt += 1 * self.speed
        else:
            if self.path:
                current = self.path[0]
                dt = self.clock.tick(60) / 1000.0
                self.move_to(current, dt)
                # Update current if we reached it
                dx = current[0] - self.true_pos[0]
                dy = current[1] - self.true_pos[1]
                if pg.math.Vector2(dx, dy).length() < 1:
                    self.path.popleft()

    def move_to(self, pos, dt):
        # Calculate distance between current pos and target, and direction
        vec = pg.math.Vector2(pos[0] - self.true_pos[0], pos[1] - self.true_pos[1])
        direction = vec.normalize()

        # Progress towards the target
        self.true_pos[0] += direction[0] * self.speed * dt
        self.true_pos[1] += direction[1] * self.speed * dt

        self.rect.center = self.true_pos

    def interact_children(self, obj1):
        i = 0
        if self.children:
            for child in self.children:
                # Skip the first tail segment
                if i == 0:
                    i += 1
                    continue
                if obj1.rect.colliderect(child):
                    obj1.die(f"Collided with {child.ID}")


class TailSegment(Entity):
    '''
    TailSegment
    ~~~~~~~~~~

    Tail Segment for the snake
    '''
    def __init__(self, screen, screen_size, base_game, ahead_obj, position):
        # Name for this type of object
        self.name = "tail-segment_"
        # Initilize parent init
        super().__init__(screen, screen_size, self.name, base_game)
        # Entity is dead or alive
        self.alive = True
        # Determines if entity can be killed
        self.killable = False
        # Obj ahead of this obj in the chain of tails/head
        self.ahead_obj = ahead_obj
        # Position in the chain of tails/head
        self.position = position
        # Where the tail was/is located
        self.prev_pos_x = ahead_obj.pos_x # was
        self.pos_x = ahead_obj.prev_pos_x # is
        if position == 0:
            self.prev_pos_y = ahead_obj.pos_y-self.size # was
            self.pos_y = ahead_obj.prev_pos_y-self.size # is
        else:
            self.prev_pos_y = ahead_obj.prev_pos_y # was
            self.pos_y = ahead_obj.prev_pos_y # is
        # Tail color = white
        self.obj_color = (255, 255, 255)

    def draw(self, screen, obj_dict):
        '''
        draw
        ~~~~~~~~~~

        draw does stuff
        '''
        if self.alive:
            # Save current position as last position
            self.prev_pos_x = self.pos_x
            self.prev_pos_y = self.pos_y
            # Where the tail is located
            self.pos_x = self.ahead_obj.prev_pos_x
            self.pos_y = self.ahead_obj.prev_pos_y
            # Set the current tail position and size
            self.obj = (self.pos_x, self.pos_y, self.size, self.size)
            # Render the tail segment based on it's parameters
            self.rect = pygame.draw.rect(screen, self.obj_color, self.obj)
