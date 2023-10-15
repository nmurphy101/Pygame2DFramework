#!/usr/bin/env python3

"""
    Decision Box


    Simple pathfinding ai for controlling entities

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from math import hypot as math_hypot
from datetime import datetime, timedelta
from inspect import currentframe, getframeinfo
from logging import warning as logging_warning
from typing import TYPE_CHECKING

from pygame import Rect
from pygame.sprite import spritecollide

from ..constants import (
    UP,
    RIGHT,
    DOWN,
    LEFT,
    UP_RIGHT,
    RIGHT_DOWN,
    DOWN_LEFT,
    LEFT_UP,
    DIRECTION_MAP,
    X,
    Y,
    NAME,
    POS_IDX,
    WIDTH,
    HEIGHT,
    TOP,
)
from ..entities import Entity, TelePortal, Line

if TYPE_CHECKING:
    from ..game import Game


class DecisionBox:
    """DecisionBox

    DecisionBox for the entity
    """


    def __init__(self, game: "Game"):
        self.game = game
        self.ai_difficulty = 10
        self.time_to_chase_target = 0
        self.portal_use_difficulty = 1
        self.farsight_use_difficulty = 1
        self.diagonal_sight_use_difficulty = 1
        self.number_open_lines = 4


    def decide_direction(self, ai_entity: Entity, target: tuple, ai_difficulty:int=None) -> int:
        """decide_direction

        Args:
            ai_entity ([Entity]): [description]
            target ([tuple]): [description]
            ai_difficulty ([int]): [description]

        Returns:
            [int]: [description]
        """

        if not target:
            return ai_entity.direction

        self.ai_difficulty = ai_difficulty or self.ai_difficulty

        # Use intent algorithm depending on ai_difficulty to decide what direction to move
        direction = self.situational_intent(ai_entity, target)

        print(f"Got Direction: {direction}")

        return direction


    def simple_intent(self, ai_entity: Entity, target: tuple) -> int:
        """simple_intent

        Args:
            ai_entity ([Entity]): [description]
            target ([tuple]): [description]

        Returns:
            [int]: [description]
        """

        # print("Simple Intent Chosen")
        intent = None

        # Equal, Right, or left  Intent
        if ai_entity.position[X] < target[POS_IDX][X]:
            intent = RIGHT

        elif ai_entity.position[X] > target[POS_IDX][X]:
            intent = LEFT

        # Equal, down, or up  Intent
        elif ai_entity.position[Y] < target[POS_IDX][Y]:
            intent = DOWN

        elif ai_entity.position[Y] > target[POS_IDX][Y]:
            intent = UP

        intent = self.check_intent(ai_entity, intent)

        # print(f"Got simple intent: {intent}")

        return intent


    def situational_intent(self, ai_entity: Entity, target: tuple) -> int:
        """situational_intent

        Args:
            ai_entity ([Entity]): [description]
            target ([tuple]): [description]

        Returns:
            [int]: [description]
        """

        # print("situational Intent Chosen")
        intent = None
        # print(ai_entity.secondary_target)
        if ai_entity.secondary_target == None:
            # down, or up  Intent
            if ai_entity.position[Y] < target[POS_IDX][Y]:
                intent = DOWN

            elif ai_entity.position[Y] > target[POS_IDX][Y]:
                intent = UP

            # Right, or left  Intent
            elif ai_entity.position[X] < target[POS_IDX][X]:
                intent = RIGHT

            elif ai_entity.position[X] > target[POS_IDX][X]:
                intent = LEFT

        else:
            # Go for secondary target within timeframe
            if datetime.now() <= ai_entity.since_secondary_target + timedelta(seconds=self.time_to_chase_target):
                # down, or up  Intent
                if ai_entity.position[Y] < ai_entity.secondary_target[POS_IDX][Y]:
                    intent = DOWN

                elif ai_entity.position[Y] > ai_entity.secondary_target[POS_IDX][Y]:
                    intent = UP

                # Right, or left  Intent
                elif ai_entity.position[X] < ai_entity.secondary_target[POS_IDX][X]:
                    intent = RIGHT

                elif ai_entity.position[X] > ai_entity.secondary_target[POS_IDX][X]:
                    intent = LEFT

            else:
                # down, or up  Intent
                if ai_entity.position[Y] < target[POS_IDX][Y]:
                    intent = DOWN

                elif ai_entity.position[Y] > target[POS_IDX][Y]:
                    intent = UP

                # Right, or left  Intent
                elif ai_entity.position[X] < target[POS_IDX][X]:
                    intent = RIGHT

                elif ai_entity.position[X] > target[POS_IDX][X]:
                    intent = LEFT

        intent = self.check_intent(ai_entity, intent)

        print(f"Got situational intent: {intent}")

        return intent


    def check_intent(self, ai_entity: Entity, intent: int) -> int:
        """check_intent

        Args:
            ai_entity ([Entity]): [description]
            intent ([int]): [description]

        Returns:
            [int]: [description]
        """

        print("Checking intent: ", intent)
        # Loop to check intent
        self.reset_sight_lines(ai_entity)
        for obj in self.game.sprite_group:
            # Ignore the target object
            if ai_entity.target[NAME] in obj.name:
                continue

            # Check if object obstructs ai_entity (and isn't self)
            if obj != ai_entity:
                print("Object checking")
                intent = self._obj_check_intent(obj, ai_entity, intent)

            # Check if object's children if any (even if self) obstructs ai_entity
            if obj.children:
                try:
                    print("child checking")
                    for child in obj.children:
                        intent = self._obj_check_intent(child, ai_entity, intent)

                except RuntimeError as error:
                    if error == "deque mutated during iteration":
                        pass

                    else:
                        frameinfo = getframeinfo(currentframe())
                        logging_warning(f"{frameinfo.filename}::{frameinfo.lineno}: WARNING: {error}")

        return intent


    def _obj_check_intent(self, other_object: Entity, ai_entity: Entity, intent: int) -> int:
        """_obj_check_intent

        Args:
            other_object ([Entity]): [description]
            ai_entity ([Entity]): [description]
            intent ([int]): [description]

        Returns:
            [int]: [description]
        """

        self.verify_sight_lines(other_object, ai_entity, intent)

        if self.number_open_lines <= 0:
            ai_entity.prev_sight_mod =  ai_entity.sight_mod
            ai_entity.sight_mod = ai_entity.sight_mod - 1
            ai_entity.sight = ai_entity.sight_mod * self.game.grid_size
            print("Reducing sight and re-verifying")
            for line in ai_entity.sight_lines:
                line.open = True
                line.draw()

            for diag_line in ai_entity.sight_lines_diag:
                line.open = True
                line.draw()

            self.verify_sight_lines(other_object, ai_entity, intent)

            ai_entity.sight_mod = ai_entity.prev_sight_mod
            ai_entity.sight = ai_entity.sight_mod * self.game.grid_size
            for line in ai_entity.sight_lines:
                line.draw()

            for diag_line in ai_entity.sight_lines_diag:
                line.draw()

        return self.get_intent(intent, ai_entity)


    def verify_sight_lines(self, other_object: Entity, ai_entity: Entity, intent: int) -> None:
        """verify_sight_lines

        Args:
            other_object ([Entity]): [description]
            ai_entity ([Entity]): [description]
            intent ([int]): [description]

        Returns:
            [None]: [description]
        """

        # Check the diagonal lines for collisions
        for diag_line in ai_entity.sight_lines_diag:
            # Check the sight lines for a open direction
            if Rect.colliderect(other_object.rect, diag_line.rect):
                print(f"It sees the collision between {other_object.id} and self on diagonal line {DIRECTION_MAP[diag_line.direction]}")
                diag_line.open = False

        # figure the current number of open lines
        self.number_open_lines = 0
        for line in ai_entity.sight_lines:
            if line.open:
                self.number_open_lines += 1

        # Verify intention with sight lines
        for line in ai_entity.sight_lines:
            if not line.open: continue

            # Check the sight lines for a open direction
            elif Rect.colliderect(other_object.rect, line.rect):
                print(f"It sees the collision between {other_object.id} and self on cardinal line {DIRECTION_MAP[line.direction]}")
                # if not "segment" in other_object.id:
                # print(f"cardinal line collision {other_object.id} and {line.direction}")
                # Will Ai see and use portals?
                if "teleportal" in other_object.name and self.ai_difficulty >= self.portal_use_difficulty:
                    line.open = self.decide_portal(other_object, ai_entity)
                    continue

                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # Edge of screen detection
            # top
            elif line.direction == UP and ai_entity.position[Y] <= self.game.screen_size[TOP]:
                print("Top edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # bottom
            elif line.direction == DOWN and ai_entity.position[Y] + ai_entity.size >= self.game.screen_size[HEIGHT]:
                print("bottom edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # left
            elif line.direction == LEFT and ai_entity.position[X] <= self.game.screen_size[LEFT]:
                print("left edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # right
            elif line.direction == RIGHT and ai_entity.position[X] + ai_entity.size >= self.game.screen_size[WIDTH]:
                print("right edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # can't move backwards
            # Up not allowed when previously having moved down
            elif line.direction == UP and ai_entity.direction == DOWN:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                print("failed line UP on can't move backwards")
                continue

            # # Down not allowed when previously having moved up
            elif line.direction == DOWN and ai_entity.direction == UP:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                print("failed line DOWN on can't move backwards")
                continue

            # # Right not allowed when previously having moved down
            elif line.direction == RIGHT and ai_entity.direction == LEFT:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                print("failed line RIGHT on can't move backwards")
                continue

            # # Left not allowed when previously having moved down
            elif line.direction == LEFT and ai_entity.direction == RIGHT:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                print("failed line LEFT on can't move backwards")
                continue

            elif other_object.parent is not None and spritecollide(line, other_object.parent.children, False):
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                print(f"Line {line.direction} definitely has some sort of collision with child obj's")
                continue

            # Verify with diagonal sight lines if available
            elif self.ai_difficulty >= self.diagonal_sight_use_difficulty and not ai_entity.sight_mod == 1:
                if line.direction == UP and intent == UP:
                    if not ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open and ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        print("failed line UP on diagonal")
                        # input(f"Press to continue: 0 - {ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open} and {ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open}")
                        continue

                elif line.direction == DOWN and intent == DOWN:
                    if not ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open and ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        print("failed line DOWN on diagonal")
                        # input(f"Press to continue: 2 - {ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open} and {ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open}")
                        continue

                elif line.direction == LEFT and intent == LEFT:
                    if not ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open and ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        print("failed line LEFT on diagonal")
                        # input(f"Press to continue: 3 - {ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open} and {ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open}")
                        continue

                elif line.direction == RIGHT and intent == RIGHT:
                    if not ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open and ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open :
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        print("failed line RIGHT on diagonal")
                        # input(f"Press to continue: 1 - {ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open} and {ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open}")
                        continue

        print(f"num open lines: {self.number_open_lines}")


    def reset_sight_lines(self, ai_entity: Entity) -> None:
        """reset_sight_lines

        Args:
            ai_entity ([Entity]): [description]

        Returns:
            [None]: [description]
        """

        for line in ai_entity.sight_lines_diag:
             line.open = True

        for line in ai_entity.sight_lines:
            line.open = True


    def get_intent(self, intent: int, ai_entity: Entity) -> int:
        """get_intent

        Args:
            intent ([int]): [description]
            ai_entity ([Entity]): [description]

        Returns:
            [int]: [description]
        """

        is_found = False
        alternate_intent = intent

        # Check which open direction to use
        for line in ai_entity.sight_lines:
            if intent == line.direction and line.open:
                is_found = True
                break

            if line.open:
                alternate_intent = line.direction

        return intent if is_found else alternate_intent


    def decide_portal(self, portal: TelePortal, ai_entity: Entity) -> bool:
        """decide_portal

        Args:
            portal ([TelePortal]): [description]
            ai_entity ([Entity]): [description]

        Returns:
            [bool]: [description]
        """

        if portal.parent:
            dist_other_portal_to_target = math_hypot(ai_entity.target[POS_IDX][X] - portal.parent.position[X], ai_entity.target[POS_IDX][Y] - portal.parent.position[Y])
            dist_self_to_target = math_hypot(ai_entity.target[POS_IDX][X] - ai_entity.position[X], ai_entity.target[POS_IDX][Y] - ai_entity.position[Y])

            if dist_other_portal_to_target < dist_self_to_target:
                if ai_entity.secondary_target:
                    return True

                ai_entity.secondary_target = (portal.position, 0, "Portal")
                self.situational_intent(ai_entity, ai_entity.target)

            else:
                return False

        else:
            dist_other_portal_to_target = math_hypot(ai_entity.target[POS_IDX][X] - portal.children[0].position[X], ai_entity.target[POS_IDX][Y] - portal.children[0].position[Y])
            dist_self_to_target = math_hypot(ai_entity.target[POS_IDX][X] - ai_entity.position[X], ai_entity.target[POS_IDX][Y] - ai_entity.position[Y])

            if dist_other_portal_to_target < dist_self_to_target:
                if ai_entity.secondary_target:
                    return True

                ai_entity.secondary_target = (portal.position, 0, "Portal")
                self.situational_intent(ai_entity, ai_entity.target)

            else:
                return False

        return False
