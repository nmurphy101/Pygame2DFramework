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
import statistics
import gc
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

class App():
    '''
    Game
    ~~~~~~~~~~

    Base game structure.
    '''
    def __init__(self, game_pkg):
        self.game_pkg = game_pkg
        self.game = None
        self.running = True
        self.fps = 300
        self.fps_list = []
        self.clock = None
        self.screen_width = 1280
        self.screen_height = 720
        self.title = "Game Platform - "
        mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        init()
        mixer.quit()
        mixer.init(44100, -16, 2, 2048)

        UI_1 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI01.wav")
        UI_2 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI02.wav")
        UI_3 = pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI03.wav")
        self.menu_sounds = [
            UI_1, UI_2, UI_3
        ]
        self.ui_sound_options = {}

    def run(self):
        '''
        run
        ~~~~~~~~~~

        run does stuff
        '''
        # Game window settings
        self.set_window_settings()
        # Game loop clock
        self.clock = pygame.time.Clock()

         # Game loop
        while self.running:
            # Send event NEXT every time music tracks ends
            mixer.music.set_endevent(NEXT)
            # Gameplay logic this turn/tick
            menu = self.game.play()
            # Update the screen display
            pygame.display.flip()
            # System/window events to be checked
            self.event_checks(menu)
            # Free unreferenced memory
            gc.collect()
            # The game loop clocktarget FPS
            self.clock.tick(self.fps)

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
        # flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        flags = 0
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)#, RESIZABLE)
        # screen.set_mode()
        alpha_screen = pygame.Surface((self.screen_width, self.screen_height)).convert_alpha()
        alpha_screen.fill([0,0,0,0])
        pygame.display.set_caption(self.title)
        screen.fill(background_colour)
        # Show game window
        pygame.display.flip()
        # Instantiate the Game Obj
        self.game = self.game_pkg(alpha_screen, screen, self)
        # Instatiate the ui sound options
        self.ui_sound_options = {
            self.game.start: 2,
            self.game.quit_game: 1,
            self.game.unpause: 1,
        }

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        _ = self.game.menu.render_button(f"now:{fps}", 11, h_offset=530)
        self.fps_list.append(int(fps))
        # Keep the fps list limited to 100 most recient samples
        if len(self.fps_list) > 200:
            self.fps_list.pop(0)
        # Average FPS
        avg_fps = str(round(statistics.mean(self.fps_list)))
        _ = self.game.menu.render_button(f"avg:{avg_fps}", 10, h_offset=530)
        # High and low FPS
        _ = self.game.menu.render_button(f"H:{max(self.fps_list)}", 8.8, h_offset=565)
        _ = self.game.menu.render_button(f"L:{min(self.fps_list)}", 7.8, h_offset=565)

    def event_checks(self, menu):
        '''
        event_checks
        ~~~~~~~~~~

        event_checks for the game
        '''
        for event in pygame.event.get():
            decision_func = {
                QUIT: lambda: self.quit,
                KEYDOWN: lambda: self.key_down(event),
                WINDOWFOCUSGAINED: lambda x=False: self.window_focus(x),
                WINDOWFOCUSLOST: lambda x=True: self.window_focus(x),
                NEXT: self.next_music,
                MOUSEBUTTONDOWN: lambda: self.mouse_down(event, menu),
            }.get(event.type)
            if decision_func:
                decision_func()

            # # Game window closes
            # if event.type == QUIT:
            #     self.running = False
            # # Press down on a key
            # elif event.type == KEYDOWN:
            #     self.key_down(event)
            # elif event.type == WINDOWFOCUSGAINED:
            #     self.game.focus_pause = False
            # elif event.type == WINDOWFOCUSLOST:
            #     self.game.focus_pause = True
            # elif event.type == NEXT:
            #     self.next_music()
            # elif event.type == MOUSEBUTTONDOWN:
            #     self.mouse_down(menu)

    def quit(self):
        self.running = False

    def window_focus(self, choice):
        self.game.focus_pause = choice

    def key_down(self, event):
        # Pressed escape to pause/unpause/back
        if event.key == K_ESCAPE:
            # If not game over
            if self.game.menu.menu_option != 3:
                self.play_ui_sound(1)
                # If already paused
                self.game.menu.menu_option = {
                    0: self.game.menu.menu_option,
                    1: None,
                    None: 1,
                }.get(self.game.menu.menu_option, self.game.menu.prev_menu)
            # If game over
            else:
                self.game.start()

    def mouse_down(self, event, menu):
        if menu:
            for button in menu:
                if button[0].collidepoint(event.pos):
                    self.play_menu_sound(button)
                    self.game.menu.prev_menu = button[2]
                    button[1]()

    def next_music(self):
        # If not game over
        if self.game.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            pygame.mixer.music.load(self.game.playlist[self.game.current_track])
            pygame.mixer.music.play(0, 0, 1)

    def play_menu_sound(self, button):
        num = self.ui_sound_options.get(button[1], 0)
        self.play_ui_sound(num)

    def play_ui_sound(self, num):
        menu_sound = self.menu_sounds[num]
        menu_sound.set_volume(float(self.game.game_config["settings"]["menu_volume"])/1.5)
        pygame.mixer.Sound.play(menu_sound)
