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
    QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, MOUSEBUTTONDOWN,
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
        self.title = "Game Platform - "
        self.music_volume = .7
        self.effect_volume = .7
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
        # self.game.start()

         # Game loop
        while self.running:
            # Gameplay logic
            menu = self.game.play()
            # System/window events to be checked
            self.event_checks(menu)
            # The game loop FPS
            clock.tick(self.fps)

        # Quit the game
        #pylint: disable=no-member
        pygame.quit()
        #pylint: enable=no-member

    def set_window_settings(self):
        '''
        set_window_settings
        ~~~~~~~~~~

        set_window_settings does stuff
        '''
        # Game window settings
        background_colour = (0, 0, 0)
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))#, RESIZABLE)
        pygame.display.set_caption(self.title)
        screen.fill(background_colour)
        game_font = freetype.Font(
            file='assets/fonts/PressStart2P-Regular.ttf',
            size=32,
        )

        # Show game window
        pygame.display.flip()

        # Instantiate the Game Obj
        self.game = self.game_pkg(screen, game_font, self)

    def event_checks(self, menu):
        '''
        event_checks
        ~~~~~~~~~~

        event_checks for the game
        '''
        for event in pygame.event.get():
            # print(event)
            # Game window closes
            if event.type == QUIT:
                self.running = False
            # Press escape to pause the game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # If not game over
                    if self.game.menu_option != 3:
                        # If already paused
                        if self.game.menu_option == 1:
                            self.game.menu_option = None
                        else:
                            self.game.menu_option = 1
                        self.game.pause_game_music = not self.game.pause_game_music
                    # Is game over
                    else:
                        self.game.menu_option = None
                        self.game.start(None)
            elif event.type == WINDOWFOCUSGAINED:
                self.game.focus_pause = False
            elif event.type == WINDOWFOCUSLOST:
                self.game.focus_pause = True
            elif event.type == MOUSEBUTTONDOWN:
                if menu:
                    for button in menu:
                        if button[0].collidepoint(event.pos):
                            self.game.prev_menu = button[2]
                            button[1](button[2])
