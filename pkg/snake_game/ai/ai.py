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
        self.portal_use_difficulty = 1
        self.time_chase = 0

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
        if entity.position[0] < target[0]:
            intent = 1
        elif entity.position[0] > target[0]:
            intent = 3
        # Equal, down, or up  Intent
        elif entity.position[1] < target[1]:
            intent = 2
        elif entity.position[1] > target[1]:
            intent = 0

        intent = self.check_intent(entity, intent)

        # print("Got simple intent")

        return intent

    def situational_intent(self, entity, target):
        # print("situational Intent Chosen")
        intent = None
        # print(entity.secondary_target)
        if entity.secondary_target == None:
            # Equal, Right, or left  Intent
            if entity.position[0] < target[0]:
                intent = 1
            elif entity.position[0] > target[0]:
                intent = 3
            # Equal, down, or up  Intent
            elif entity.position[1] < target[1]:
                intent = 2
            elif entity.position[1] > target[1]:
                intent = 0
        else:
            # Go for secondary target within timeframe
            if datetime.now() <= entity.since_secondary_target + timedelta(seconds=self.time_chase):
                # Equal, Right, or left  Intent
                if entity.position[0] < entity.secondary_target[0]:
                    intent = 1
                elif entity.position[0] > entity.secondary_target[0]:
                    intent = 3
                # Equal, down, or up  Intent
                elif entity.position[1] < entity.secondary_target[1]:
                    intent = 2
                elif entity.position[1] > entity.secondary_target[1]:
                    intent = 0
            else:
                # Equal, Right, or left  Intent
                if entity.position[0] < target[0]:
                    intent = 1
                elif entity.position[0] > target[0]:
                    intent = 3
                # Equal, down, or up  Intent
                elif entity.position[1] < target[1]:
                    intent = 2
                elif entity.position[1] > target[1]:
                    intent = 0

        intent = self.check_intent(entity, intent)

        # print("Got situational intent")

        return intent

    def check_intent(self, entity, intent):
        # print("Checking intent: ", intent)
        # eval func's only once before loops
        verify_sight_lines = self.verify_sight_lines
        get_intent = self.get_intent
        reset_sight_lines = self.reset_sight_lines
        decide_portal = self.decide_portal
        collide_rect = pygame.sprite.collide_rect
        situational_intent = self.situational_intent
        hypot = math.hypot
        # Loop to check intent
        while 1:
            reset_sight_lines(entity)
            for obj in self.obj_container:
                # Ignore the target object
                if entity.target != obj.position:
                # if "food" not in obj.name:
                    # Check if object obstructs entity (and isn't self)
                    if obj != entity:
                        verify_sight_lines(obj, entity, decide_portal, collide_rect, situational_intent, hypot)
                        intent = get_intent(intent, entity)
                    # Check if object's children if any (even if self) obstructs entity
                    if obj.children:
                        for child in obj.children:
                            verify_sight_lines(child, entity, decide_portal, collide_rect, situational_intent, hypot)
                            intent = get_intent(intent, entity)
            # Break from while loop
            break

        # print(f"Returning Found Intent: {intent}")
        return intent

    def verify_sight_lines(self, obj, entity, decide_portal, collide_rect, situational_intent, hypot):
        # Verify intention with sight lines
        for line in entity.sight_lines:
            # Edge of screen detection
            if line.direction == 0 and line.end[1] <= 0:
                line.open = False
            elif line.direction == 2 and line.end[1] >= entity.screen_size[1]:
                line.open = False
            elif line.direction == 3 and line.end[0] <= 0:
                line.open = False
            elif line.direction == 1 and line.end[0] >= entity.screen_size[0]:
                line.open = False
            # Check the sight lines for a open direction
            if collide_rect(obj, line):
                # Will Ai see and use portals?
                if "teleportal" in obj.name and self.difficulty >= self.portal_use_difficulty:
                    line.open = decide_portal(obj, entity, situational_intent, hypot)
                else:
                    line.open = False

    def reset_sight_lines(self, entity):
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

    def decide_portal(self, obj, entity, situational_intent, hypot):
        if obj.parent:
            dist_oth_portal = hypot(entity.target[0] - obj.parent.position[0], entity.target[1] - obj.parent.position[1])
            dist_self = hypot(entity.target[0] - entity.position[0], entity.target[1] - entity.position[1])
            if dist_oth_portal < dist_self:
                if entity.secondary_target:
                    return True
                else:
                    entity.secondary_target = obj.position
                    situational_intent(entity, entity.target)
            else:
                return False
        else:
            dist_oth_portal = hypot(entity.target[0] - obj.children[0].position[0], entity.target[1] - obj.children[0].position[1])
            dist_self = hypot(entity.target[0] - entity.position[0], entity.target[1] - entity.position[1])
            if dist_oth_portal < dist_self:
                if entity.secondary_target:
                    return True
                else:
                    entity.secondary_target = obj.position
                    situational_intent(entity, entity.target)
            else:
                return False
        return False
