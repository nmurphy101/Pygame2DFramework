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
from logging import(
    debug as logging_debug,
    warning as logging_warning,
)
from typing import TYPE_CHECKING

from pygame import Rect
from pygame.sprite import spritecollide

from ..ai.node import Node
from ..ai.helpers import astar, obj_pos_to_node
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
        self.a_star_use_difficulty = 1
        self.a_star_situational_backup_difficulty = 2
        self.diagonal_sight_use_difficulty = 1
        self.number_open_lines = 4
        self.default_node = Node(x=-1, y=-1, walkable=False)


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

        logging_debug(f"Got Direction: {direction}")

        return direction


    def simple_intent(self, ai_entity: Entity, target: tuple) -> int:
        """simple_intent

        Args:
            ai_entity ([Entity]): [description]
            target ([tuple]): [description]

        Returns:
            [int]: [description]
        """

        logging_debug("Simple Intent Chosen")
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

        logging_debug(f"Got simple intent: {intent}")

        return intent


    def situational_intent(self, ai_entity: Entity, target: tuple) -> int:
        """situational_intent

        Args:
            ai_entity ([Entity]): [description]
            target ([tuple]): [description]

        Returns:
            [int]: [description]
        """

        logging_debug("situational Intent Chosen")
        intent = None
        logging_debug(ai_entity.secondary_target)
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

        logging_debug(f"Got situational intent: {intent}")

        return intent


    def astar_intent(self, ai_entity, target):
        # Get the start and end node
        start_node = obj_pos_to_node(self.game, ai_entity.position)
        end_node = obj_pos_to_node(self.game, target[POS_IDX])

        # Continue with cached path or calculate a new one

        logging_debug(ai_entity.id, ai_entity.path)

        logging_debug("Entity position: ", (ai_entity.position[X]//self.game.grid_size, ai_entity.position[Y]//self.game.grid_size))
        logging_debug("Target position: ", (target[POS_IDX][X]//self.game.grid_size, target[POS_IDX][Y]//self.game.grid_size))

        try:
            ai_entity.path.pop(0)

        except IndexError:
            pass

        next_node = self.game.grid[ai_entity.path[0][X]][ai_entity.path[0][Y]] if ai_entity.path and not ai_entity.path == [] else self.default_node

        logging_debug(((next_node.x, next_node.y), next_node.walkable) if next_node else logging_debug("NA"))
        logging_debug(f"Node walkable? {(next_node.walkable, next_node.x, next_node.y, ai_entity.path) if ai_entity.path else ai_entity.path}")

        if ai_entity.path == [] or not next_node.walkable:
            # Get the path to target via astar pathfinding algorithm
            ai_entity.path = astar(self.game, start_node, end_node)


        # TODO: Validate on difficulty check if the next move will trap self by checking the next a_star ai_entity.path

        # In case the snake has no valid route use backup logic
        if not ai_entity.path:
            if self.ai_difficulty > self.a_star_use_difficulty:
                return self.situational_intent(ai_entity, target)
            else:
                return self.simple_intent(ai_entity, target)

        next_pos = (ai_entity.path[0][X] * self.game.grid_size,  ai_entity.path[0][Y] * self.game.grid_size)

        # UP
        if next_pos[X] == ai_entity.position[X] and next_pos[Y] < ai_entity.position[Y]:
            return UP

        # DOWN
        elif next_pos[X] == ai_entity.position[X] and next_pos[Y] > ai_entity.position[Y]:
            return DOWN

        # LEFT
        elif next_pos[X] < ai_entity.position[X] and next_pos[Y] == ai_entity.position[Y]:
            return LEFT

        # RIGHT
        elif next_pos[X] > ai_entity.position[X] and next_pos[Y] == ai_entity.position[Y]:
            return RIGHT

        # Get the intent of the next direction
        else:
            logging_debug(f"Was unable to find the direction from the A_star position: {next_pos}")
            pass


    def astar_verification(self, ai_entity, next_target):
        # Get the start and end node
        start_node = obj_pos_to_node(self.game, ai_entity.target[POS_IDX])
        end_node = obj_pos_to_node(self.game, next_target[POS_IDX])

        return True if astar(self.game, start_node, end_node) else False


    def check_intent(self, ai_entity: Entity, intent: int) -> int:
        """check_intent

        Args:
            ai_entity ([Entity]): [description]
            intent ([int]): [description]

        Returns:
            [int]: [description]
        """

        logging_debug(f"Checking intent: {intent}")
        # Loop to check intent
        self.reset_sight_lines(ai_entity)
        for obj in self.game.sprite_group:
            # Ignore the target object
            if ai_entity.target[NAME] in obj.name:
                continue

            # Check if object obstructs ai_entity (and isn't self)
            if obj != ai_entity:
                logging_debug("Object checking")
                intent = self._obj_check_intent(obj, ai_entity, intent)

            # Check if object's children if any (even if self) obstructs ai_entity
            if obj.children:
                try:
                    logging_debug("child checking")
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

        # No directions could be found so reduce entity sight and check again
        if self.number_open_lines <= 0:
            ai_entity.prev_sight_mod =  ai_entity.sight_mod
            ai_entity.sight_mod = ai_entity.sight_mod - 1
            ai_entity.sight = ai_entity.sight_mod * self.game.grid_size
            logging_debug("Reducing sight and re-verifying")
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
                logging_debug(f"It sees the collision between {other_object.id} and self on diagonal line {DIRECTION_MAP[diag_line.direction]}")
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
                logging_debug(f"It sees the collision between {other_object.id} and self on cardinal line {DIRECTION_MAP[line.direction]}")
                # if not "segment" in other_object.id:
                logging_debug(f"cardinal line collision {other_object.id} and {line.direction}")
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
                logging_debug("Top edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # bottom
            elif line.direction == DOWN and ai_entity.position[Y] + ai_entity.size >= self.game.screen_size[HEIGHT]:
                logging_debug("bottom edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # left
            elif line.direction == LEFT and ai_entity.position[X] <= self.game.screen_size[LEFT]:
                logging_debug("left edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # right
            elif line.direction == RIGHT and ai_entity.position[X] + ai_entity.size >= self.game.screen_size[WIDTH]:
                logging_debug("right edge collision predicted")
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                continue

            # can't move backwards
            # Up not allowed when previously having moved down
            elif line.direction == UP and ai_entity.direction == DOWN:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                logging_debug("failed line UP on can't move backwards")
                continue

            # # Down not allowed when previously having moved up
            elif line.direction == DOWN and ai_entity.direction == UP:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                logging_debug("failed line DOWN on can't move backwards")
                continue

            # # Right not allowed when previously having moved down
            elif line.direction == RIGHT and ai_entity.direction == LEFT:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                logging_debug("failed line RIGHT on can't move backwards")
                continue

            # # Left not allowed when previously having moved down
            elif line.direction == LEFT and ai_entity.direction == RIGHT:
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                logging_debug("failed line LEFT on can't move backwards")
                continue

            elif other_object.parent is not None and spritecollide(line, other_object.parent.children, False):
                line.open = False
                self.number_open_lines = self.number_open_lines - 1
                logging_debug(f"Line {line.direction} definitely has some sort of collision with child obj's")
                continue

            # Verify with diagonal sight lines if available
            elif self.ai_difficulty >= self.diagonal_sight_use_difficulty and not ai_entity.sight_mod == 1:
                if line.direction == UP and intent == UP:
                    if not ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open and not ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        logging_debug("failed line UP on diagonal")
                        # input(f"Press to continue: 0 - {ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open} and {ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open}")
                        continue

                elif line.direction == DOWN and intent == DOWN:
                    if not ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open and not ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        logging_debug("failed line DOWN on diagonal")
                        # input(f"Press to continue: 2 - {ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open} and {ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open}")
                        continue

                elif line.direction == LEFT and intent == LEFT:
                    if not ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open and not ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        logging_debug("failed line LEFT on diagonal")
                        # input(f"Press to continue: 3 - {ai_entity.sight_lines_diag[int(LEFT_UP-.5)].open} and {ai_entity.sight_lines_diag[int(DOWN_LEFT-.5)].open}")
                        continue

                elif line.direction == RIGHT and intent == RIGHT:
                    if not ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open and not ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open:
                        line.open = False
                        self.number_open_lines = self.number_open_lines - 1
                        logging_debug("failed line RIGHT on diagonal")
                        # input(f"Press to continue: 1 - {ai_entity.sight_lines_diag[int(RIGHT_DOWN-.5)].open} and {ai_entity.sight_lines_diag[int(UP_RIGHT-.5)].open}")
                        continue

            # TODO: Check for dead end routes via the game grid nodes

        logging_debug(f"num open lines: {self.number_open_lines}")


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
