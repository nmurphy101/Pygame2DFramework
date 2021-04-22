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
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE,
    WINDOWFOCUSGAINED, WINDOWFOCUSLOST,
)
# pylint: enable=no-name-in-module

class BaseGame():
    '''
    Game
    ~~~~~~~~~~

    Base game structure.
    '''
    def __init__(self, game_pkg):
        self.game_pkg = game_pkg
        self.game = None
        self.running = True
        self.fps = 60
        self.screen_width = 1280
        self.screen_height = 720
        self.title = "SnakeAI"
        init()

    def run(self):
        '''
        run
        ~~~~~~~~~~

        run does stuff
        '''
        # Game window settings
        self.set_window_settings()

        clock = pygame.time.Clock()

        # Initilize game objects
        self.game.start()

         # Game loop
        while self.running:
            # System/window events to be checked
            self.event_checks()

            # Gameplay logic
            self.game.play()

            # The game loop FPS
            clock.tick(self.fps)

        # pylint: disable=no-member
        pygame.quit()
        # pylint: enable=no-member

    def set_window_settings(self):
        ''' 
        set_window_settings
        ~~~~~~~~~~

        set_window_settings does stuff
        '''
        # Game window settings
        background_colour = (0, 0, 0)
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.title)
        screen.fill(background_colour)
        game_font = freetype.Font(
            file='assets/fonts/PressStart2P-Regular.ttf',
            size=32,
        )

        # Show game window
        pygame.display.flip()

        # Instantiate the Game Obj
        self.game = self.game_pkg(screen, game_font)

    def event_checks(self):
        for event in pygame.event.get():
            # print(event)
            # Game window closes
            if event.type == QUIT:
                self.running = False
            # Press escape to pause the game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if not self.game.game_over:
                        self.game.pause = not self.game.pause
                    else:
                        self.game.game_over = False
                        self.game.start()
            elif event.type == WINDOWFOCUSGAINED:
                self.game.focus_pause = False
            elif event.type == WINDOWFOCUSLOST:
                self.game.focus_pause = True
