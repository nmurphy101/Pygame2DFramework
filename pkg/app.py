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
    init, mixer
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
        self.fps = 1000
        self.fps_list = []
        self.fps_pos = None
        self.fps_rect = None
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
        self.pause_menu_options = {}
        # event = None
        # menu = None
        self.event_options = {
            QUIT: lambda **kwargs: self.quit(**kwargs),
            NEXT: lambda **kwargs: self.next_music(**kwargs),
            WINDOWFOCUSGAINED: lambda **kwargs: self.window_focus(focus=False, **kwargs),
            WINDOWFOCUSLOST: lambda **kwargs: self.window_focus(focus=True, **kwargs),
            KEYDOWN: lambda **kwargs: self.key_down(**kwargs),
            MOUSEBUTTONDOWN: lambda **kwargs: self.mouse_down(**kwargs),
        }
        events = []
        for event in self.event_options.keys():
            events.append(event)
        # Limit the type of game events that can happen
        pygame.event.set_allowed(events)

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
        # eval func's only once before loops
        event_get = self.event_options.get
        update_fps = self.update_fps
        play = self.game.play
        event_checks = self.event_checks
        update = pygame.display.update
        set_endevent = mixer.music.set_endevent
        tick = self.clock.tick

         # Game loop
        while self.running:
            # The game loop clocktarget FPS
            tick(self.fps)
            # Send event NEXT every time music tracks ends
            set_endevent(NEXT)
            # Gameplay logic this turn/tick
            menu, dirty_rects = play(update_fps)
            if dirty_rects:
                # Update the screen display
                update(dirty_rects)
                # reset loop variables
                self.dirty_rects = []
            elif menu:
                # Update the screen display
                update()
            # System/window events to be checked
            event_checks(menu, event_get)
            # Free unreferenced memory
            # gc.collect()

    def set_window_settings(self):
        '''
        set_window_settings
        ~~~~~~~~~~

        set_window_settings does stuff
        '''
        # Game window settings
        background_colour = (0, 0, 0)
        flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN |
        # flags = 0
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags, 16)#, RESIZABLE)
        # screen.set_mode()
        alpha_screen = pygame.Surface((self.screen_width, self.screen_height)).convert_alpha()
        alpha_screen.fill([0,0,0,0])
        pygame.display.set_caption(self.title)
        screen.fill(background_colour)
        # Show game window
        pygame.display.flip()
        # Instantiate the Game Obj
        self.game = self.game_pkg(alpha_screen, screen, self)
        # Instatiate options dict's
        self.ui_sound_options = {
            self.game.start: 2,
            self.game.quit_game: 1,
            self.game.unpause: 1,
        }
        self.pause_menu_options = {
            0: self.game.menu.menu_option,
            1: None,
            None: 1,
        }
        self.fps_pos = (self.game.screen_size[0]/2-(8*self.game.game_font.size)/2 + 545,
                        self.game.screen_size[1]/2 - self.game.game_font.size * 11.5,
                        250, 138)
        self.fps_rect = pygame.Rect(self.fps_pos)

    def update_fps(self):
        # Clear previous frame obj's location
        self.game.screen.fill((0, 0, 0, 0), self.fps_pos)
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
        return self.fps_rect

    def event_checks(self, menu, event_get):
        '''
        event_checks
        ~~~~~~~~~~

        event_checks for the game
        '''
        for event in pygame.event.get():
            # Possible event options:
            #   QUIT, NEXT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST,  KEYDOWN, MOUSEBUTTONDOWN,
            decision_func = event_get(event.type)
            if decision_func:
                decision_func(event=event, menu=menu)

    def quit(self, **_):
        self.running = False

    def window_focus(self, focus, **_):
        self.game.focus_pause = focus

    def key_down(self, **kwargs):
        # Pressed escape to pause/unpause/back
        if kwargs["event"].key == K_ESCAPE:
            # If not game over
            if self.game.menu.menu_option != 3:
                self.play_ui_sound(1)
                # Either unpause or pause the game
                self.game.menu.prev_menu = self.game.menu.menu_option
                self.game.menu.menu_option = self.pause_menu_options.get(self.game.menu.menu_option, self.game.menu.prev_menu)
            # If game over
            else:
                self.game.start()

    def mouse_down(self, **kwargs):
        if kwargs["menu"]:
            for button in kwargs["menu"]:
                if button[0].collidepoint(kwargs["event"].pos):
                    self.play_menu_sound(button)
                    self.game.menu.prev_menu = button[2]
                    button[1]()

    def next_music(self, **_):
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
        menu_sound.set_volume(float(self.game.game_config["settings"]["sound"]["menu_volume"])/1.5)
        pygame.mixer.Sound.play(menu_sound)
