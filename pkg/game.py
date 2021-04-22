#!/usr/bin/env python3

'''
    Game App
    ~~~~~~~~~~

    Base for a game in a window

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


# import os
# import threading
# import logging
# import sys
# import time
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import pygame
# pylint: disable=no-name-in-module
from pygame import (
    freetype, init
)
# pylint: enable=no-name-in-module

class BaseGame():
    '''
    Game
    ~~~~~~~~~~

    Base game structure.
    '''
    def __init__(self, game_obj):
        self.game_obj = game_obj
        init()

    def run(self):
        '''
        run
        ~~~~~~~~~~

        run does stuff
        '''
        # Game window settings
        game = self.set_window_settings()

        # Start the game loop
        game.play()

    def set_window_settings(self):
        '''
        set_window_settings
        ~~~~~~~~~~

        set_window_settings does stuff
        '''
        # Game window settings
        (width, height) = (1280, 720)
        background_colour = (0, 0, 0)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('SnakeAI')
        screen.fill(background_colour)
        game_font = freetype.Font(
            file='assets/fonts/PressStart2P-Regular.ttf',
            size=32,
        )

        # Show game window
        pygame.display.flip()

        # Instantiate the Game Obj
        game = self.game_obj(screen, game_font)

        # Return window objects
        return game
