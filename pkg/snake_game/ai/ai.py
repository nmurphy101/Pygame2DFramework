#!/usr/bin/env python3

'''
    Simple Pathfinding
    ~~~~~~~~~~

    Simple pathfinding ai for controlling entities


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import math
from datetime import datetime, timedelta

import pygame


class DecisionBox:
    '''
    DecisionBox
    ~~~~~~~~~~

    DecisionBox for the entity
    '''

    def __init__(self):
        self.difficulty = None
        self.obj_container = None
        self.time_chase = 0
        self.portal_use_difficulty = 1
        self.farsight_use_difficulty = 1

    def decide_direction(self, entity, target, obj_container, difficulty=0):
        if not target:
            return entity.direction

        self.difficulty = difficulty
        self.obj_container = obj_container
        # Use intent algorithm depending on difficulty
        direction = self.situational_intent(entity, target)

        # print("Got Direction")

        return direction


    def simple_intent(self, entity, target):
        # print("Simple Intent Chosen")
        intent = None

        # Equal, Right, or left  Intent
        if entity.position[0] < target[1]:
            intent = 1

        elif entity.position[0] > target[1]:
            intent = 3

        # Equal, down, or up  Intent
        elif entity.position[1] < target[2]:
            intent = 2

        elif entity.position[1] > target[2]:
            intent = 0

        intent = self.check_intent(entity, intent)

        # print("Got simple intent")

        return intent


    def situational_intent(self, entity, target):
        # print("situational Intent Chosen")
        intent = None
        # print(entity.secondary_target)
        if entity.secondary_target == None:
            # Equal, down, or up  Intent
            if entity.position[1] < target[2]:
                intent = 2

            elif entity.position[1] > target[2]:
                intent = 0

            # Equal, Right, or left  Intent
            elif entity.position[0] < target[1]:
                intent = 1

            elif entity.position[0] > target[1]:
                intent = 3

        else:
            # Go for secondary target within timeframe
            if datetime.now() <= entity.since_secondary_target + timedelta(seconds=self.time_chase):
                # Equal, down, or up  Intent
                if entity.position[1] < entity.secondary_target[1]:
                    intent = 2

                elif entity.position[1] > entity.secondary_target[1]:
                    intent = 0

                # Equal, Right, or left  Intent
                elif entity.position[0] < entity.secondary_target[0]:
                    intent = 1

                elif entity.position[0] > entity.secondary_target[0]:
                    intent = 3

            else:
                # Equal, down, or up  Intent
                if entity.position[1] < target[2]:
                    intent = 2

                elif entity.position[1] > target[2]:
                    intent = 0

                # Equal, Right, or left  Intent
                elif entity.position[0] < target[1]:
                    intent = 1

                elif entity.position[0] > target[1]:
                    intent = 3

        intent = self.check_intent(entity, intent)

        # print("Got situational intent")

        return intent


    def check_intent(self, entity, intent):
        # print("Checking intent: ", intent)
        # Loop to check intent
        self.reset_sight_lines(entity)
        for obj in self.obj_container:
            # Ignore the target object
            if entity.target[0] not in obj.name:
            # if "food" not in obj.name:

                # Check if object obstructs entity (and isn't self)
                if obj != entity:
                    self.verify_sight_lines(obj, entity, intent)
                    intent = self.get_intent(intent, entity)

                # Check if object's children if any (even if self) obstructs entity
                if obj.children:
                    for child in obj.children:
                        self.verify_sight_lines(child, entity, intent)
                        intent = self.get_intent(intent, entity)

        # print(f"Returning Found Intent: {intent}")
        return intent


    def verify_sight_lines(self, obj, entity, intent):
        for line in entity.sight_lines_diag:
            # Check the sight lines for a open direction
            if pygame.Rect.collidepoint(obj.rect, line.end):
                line.open = False

            # Edge of screen detection
            elif line.end[1] <= 0:
                line.open = False

            elif line.end[1] >= entity.screen_size[1]:
                line.open = False

            elif line.end[0] <= 0:
                line.open = False

            elif line.end[0] >= entity.screen_size[0]:
                line.open = False

        # Verify intention with sight lines
        for line in entity.sight_lines:
            # Check the sight lines for a open direction
            if pygame.Rect.colliderect(obj.rect, line.rect):
                # if not "segment" in obj.ID:
                # print(f"cardinal line collision {obj.ID} and {line.direction}")
                # Will Ai see and use portals?
                if "teleportal" in obj.name and self.difficulty >= self.portal_use_difficulty:
                    line.open = self.decide_portal(obj, entity)

                else:
                    line.open = False
                    continue

            # Edge of screen detection
            elif line.direction == 0 and line.end[1] <= (0 - entity.size):
                line.open = False
                continue

            elif line.direction == 2 and line.end[1] >= (entity.screen_size[1] + entity.size):
                line.open = False
                continue

            elif line.direction == 3 and line.end[0] <= (0 - entity.size):
                line.open = False
                continue

            elif line.direction == 1 and line.end[0] >= (entity.screen_size[0] + entity.size):
                line.open = False
                continue

            # Verify with farsight sight lines
            if entity.sight_lines_diag != [] and self.difficulty >= self.farsight_use_difficulty:
                if line.direction == 0 and intent == 0:
                    if not entity.sight_lines_diag[0].open and not entity.sight_lines_diag[3].open:
                        line.open = False
                        # input(f"Press to continue: 0 - {entity.sight_lines_diag[0].open} and {entity.sight_lines_diag[3].open}")
                        continue

                elif line.direction == 2 and intent == 2:
                    if not entity.sight_lines_diag[2].open and not entity.sight_lines_diag[1].open:
                        line.open = False
                        # input(f"Press to continue: 2 - {entity.sight_lines_diag[2].open} and {entity.sight_lines_diag[1].open}")
                        continue

                elif line.direction == 3 and intent == 3:
                    if not entity.sight_lines_diag[3].open and not entity.sight_lines_diag[2].open:
                        line.open = False
                        # input(f"Press to continue: 3 - {entity.sight_lines_diag[3].open} and {entity.sight_lines_diag[2].open}")
                        continue

                elif line.direction == 1 and intent == 1:
                    if not entity.sight_lines_diag[1].open and not entity.sight_lines_diag[0].open :
                        line.open = False
                        # input(f"Press to continue: 1 - {entity.sight_lines_diag[1].open} and {entity.sight_lines_diag[0].open}")
                        continue


    def reset_sight_lines(self, entity):
        for line in entity.sight_lines_diag:
             line.open = True

        for line in entity.sight_lines:
            line.open = True


    def get_intent(self, intent, entity):
        # Check which open direction to use
        for line in entity.sight_lines:
            if intent == line.direction and line.open:
                if line.direction == 0 and entity.direction != 2:
                    # print(f"Original Line {line.direction} is open")
                    # break inner line for-loop
                    break

                elif line.direction == 2 and entity.direction != 0:
                    # print(f"Original Line {line.direction} is open")
                    # break inner line for-loop
                    break

                elif line.direction == 3 and entity.direction != 1:
                    # print(f"Original Line {line.direction} is open")
                    # break inner line for-loop
                    break

                elif line.direction == 1 and entity.direction != 3:
                    # print(f"Original Line {line.direction} is open")
                    # break inner line for-loop
                    break

                # else:
                    # print(f"Original Line {line.direction} is closed")

            elif intent == line.direction and not line.open:
                # Find a different line to use
                for line2 in entity.sight_lines:
                    if intent != line2.direction and line2.open:
                        if line2.direction == 0 and entity.direction != 2:
                            intent = line2.direction
                            # print(f"New Line {line.direction} is open")
                            # break inner line for-loop
                            break

                        elif line2.direction == 2 and entity.direction != 0:
                            intent = line2.direction
                            # print(f"New Line {line.direction} is open")
                            # break inner line for-loop
                            break

                        elif line2.direction == 3 and entity.direction != 1:
                            intent = line2.direction
                            # print(f"New Line {line.direction} is open")
                            # break inner line for-loop
                            break

                        elif line2.direction == 1 and entity.direction != 3:
                            intent = line2.direction
                            # print(f"New Line {line.direction} is open")
                            # break inner line for-loop
                            break

                        # else:
                            # print("Couldn't get a different open line")

        return intent


    def decide_portal(self, obj, entity):
        """AI is creating summary for decide_portal

        Args:
            obj ([type]): [description]
            entity ([type]): [description]

        Returns:
            [type]: [description]
        """

        if obj.parent:
            dist_oth_portal = math.hypot(entity.target[1] - obj.parent.position[0], entity.target[2] - obj.parent.position[1])
            dist_self = math.hypot(entity.target[1] - entity.position[0], entity.target[2] - entity.position[1])

            if dist_oth_portal < dist_self:
                if entity.secondary_target:
                    return True

                entity.secondary_target = obj.position
                self.situational_intent(entity, entity.target)

            else:
                return False

        else:
            dist_oth_portal = math.hypot(entity.target[1] - obj.children[0].position[0], entity.target[2] - obj.children[0].position[1])
            dist_self = math.hypot(entity.target[1] - entity.position[0], entity.target[2] - entity.position[1])
            if dist_oth_portal < dist_self:
                if entity.secondary_target:
                    return True

                entity.secondary_target = obj.position
                self.situational_intent(entity, entity.target)

            else:
                return False

        return False
