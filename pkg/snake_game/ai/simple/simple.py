#!/usr/bin/env python3

'''
    Simple Pathfinding
    ~~~~~~~~~~

    Simple pathfinding ai for controlling entities


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''




class SimpleSearch:
    '''
    SimpleSearch
    ~~~~~~~~~~

    SimpleSearch for the entity
    '''
    def __init__(self):
        pass

    def decide_direction(self, entity, target):
        intent = None
        # Equal, Right, or left  Intent
        print(entity.pos_x, target[0])
        if entity.pos_x < target[0]:
            intent = 1
        elif entity.pos_x > target[0]:
            intent = 3
        # Equal, down, or up  Intent
        elif entity.pos_y < target[1]:
            intent = 2
        elif entity.pos_y > target[1]:
            intent = 0

        # Check if Intent is actionable direction
        if intent == 3 and entity.prev_direction != 1:
            return 3
        elif intent == 1 and entity.prev_direction != 3:
            return 1
        # Check if Intent is actionable direction
        elif intent == 0 and entity.prev_direction != 2:
            return 0
        elif intent == 2 and entity.prev_direction != 0:
            return 2

        return entity.direction
