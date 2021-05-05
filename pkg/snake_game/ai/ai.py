#!/usr/bin/env python3

'''
    Simple Pathfinding
    ~~~~~~~~~~

    Simple pathfinding ai for controlling entities


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame

class DecisionBox:
    '''
    DecisionBox
    ~~~~~~~~~~

    DecisionBox for the entity
    '''
    def __init__(self):
        pass

    def decide_direction(self, entity, target, obj_dict, difficulty=0):
        self.obj_dict = obj_dict
        # Use intent algorithm depending on difficulty
        if difficulty != 0:
            direction = self.simple_intent(entity, target)
        else:
            direction = self.simple_intent(entity, target)

        # print("Got Direction")

        return direction


    def simple_intent(self, entity, target):
        # print("Simple Intent Chosen")
        intent = None
        # Equal, Right, or left  Intent
        if entity.pos_x < target[0]:
            intent = 1
        elif entity.pos_x > target[0]:
            intent = 3
        # Equal, down, or up  Intent
        elif entity.pos_y < target[1]:
            intent = 2
        elif entity.pos_y > target[1]:
            intent = 0

        intent = self.check_intent(entity, intent)

        # print("Got simple intent")

        return intent

    def check_intent(self, entity, intent):
        # print("Checking intent: ", intent)
        ori_intent = intent
        while True:
            self.reset_sight_lines(entity)
            for name, obj in self.obj_dict.items():
                # Ignore the target object
                if entity.target != (obj.pos_x, obj.pos_y):
                    # Check if object obstructs entity
                    if obj != entity:
                        ori_intent = intent
                        self.verify_sight_lines(obj, entity)
                        intent = self.get_intent(intent, entity)
                    # Check if object's children if any (even if self) obstructs entity
                    if obj.children:
                        ori_intent = intent
                        for child in obj.children:
                            self.verify_sight_lines(child, entity)
                            intent = self.get_intent(intent, entity)
                            # if intent != ori_intent:
                                # print(f"intent changed on child: {ori_intent} to {intent}")
            # Break from while loop
            break

        # print(f"Returning Found Intent: {intent}")
        return intent

    def verify_sight_lines(self, obj, entity):
        # Verify intention with sight lines
        for line in entity.sight_lines:
            # Edge of screen detection
            if line.direction == 0 and line.end[1] < 0 - entity.size:
                line.open = False
            elif line.direction == 3 and line.end[1] < 0 - entity.size:
                line.open = False
            elif line.direction == 2 and line.end[1] > entity.screen_size[1] + entity.size:
                line.open = False
            elif line.direction == 1 and line.end[1] > entity.screen_size[0] + entity.size:
                line.open = False
            # Check the sight lines for a open direction
            if obj.rect.colliderect(line):
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
