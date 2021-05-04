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
    freetype, init, mixer
)
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, MOUSEBUTTONDOWN,
    WINDOWFOCUSGAINED, WINDOWFOCUSLOST, USEREVENT
)
# pylint: enable=no-name-in-module

NEXT = USEREVENT + 1

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
        self.music_volume = .2
        self.effect_volume = .4
        self.menu_volume = .4
        mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        init()
        mixer.quit()
        mixer.init(44100, -16, 2, 2048)

        UI1 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI01.wav")
        UI2 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI02.wav")
        UI3 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI03.wav")
        self.menu_sounds = [
            UI1, UI2, UI3
        ]

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
            # Send event NEXT every time music tracks ends
            mixer.music.set_endevent(NEXT)
            # Gameplay logic
            menu = self.game.play()
            # System/window events to be checked
            self.event_checks(menu)
            # The game loop FPS
            clock.tick(self.fps)

        #pylint: disable=no-member
        # Quit the game
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
            # Game window closes
            if event.type == QUIT:
                self.running = False
            # Press escape to pause/unpause/back
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # If not game over
                    if self.game.menu.menu_option != 3:
                        self.play_UI(1)
                        # If already paused
                        if self.game.menu.menu_option == 1:
                            self.game.menu.menu_option = None
                        elif self.game.menu.menu_option is None:
                            self.game.menu.menu_option = 1
                        elif self.game.menu.menu_option != 0:
                            self.game.menu.menu_option = self.game.menu.prev_menu
                    # If game over
                    else:
                        self.game.start()
            elif event.type == WINDOWFOCUSGAINED:
                self.game.focus_pause = False
            elif event.type == WINDOWFOCUSLOST:
                self.game.focus_pause = True
            elif event.type == NEXT:
                # If not game over
                if self.game.menu.menu_option != 3:
                    # Get next track (modulo number of tracks)
                    self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
                    pygame.mixer.music.load(self.game.playlist[self.game.current_track])
                    pygame.mixer.music.play(0, 0, 1)
            elif event.type == MOUSEBUTTONDOWN:
                if menu:
                    for button in menu:
                        if button[0].collidepoint(event.pos):
                            self.play_menu_sound(button)
                            self.game.menu.prev_menu = button[2]
                            button[1]()

    def play_menu_sound(self, button):
        if button[1] == self.game.start:
            self.play_UI(2)
        elif button[1] == self.game.quit_game:
            self.play_UI(1)
        elif button[1] == self.game.unpause:
            self.play_UI(1)
        else:
            self.play_UI(0)

    def play_UI(self, num):
        menu_sound = self.menu_sounds[num]
        menu_sound.set_volume(self.menu_volume/1.5)
        pygame.mixer.Sound.play(menu_sound)
