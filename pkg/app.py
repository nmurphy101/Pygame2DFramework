#!/usr/bin/env python3

'''
    Game App
    ~~~~~~~~~~

    Base for a game in a window

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''


import os
# import threading
# import logging
# import sys
# import time
# import re
# import queue as q
# from multiprocessing import Pool, cpu_count, Queue, Process, Manager, Lock
import statistics
import json
import pygame
# pylint: disable=no-name-in-module
from pygame import (
    init, mixer, DOUBLEBUF, FULLSCREEN
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
        mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        init()
        mixer.quit()
        mixer.init(44100, -16, 2, 2048)

        self.game_pkg = game_pkg
        self.game = None
        self.running = True
        self.fps = 3000
        self.fps_list = []
        self.fps_pos = None
        self.fps_rect = None
        self.clock = None
        self.title = "Game Platform - "
        self.screen = None
        self.debug_screen = None
        self.background_0 = None

        self.menu_sounds = [
            pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI01.wav"), # hover
            pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI02.wav"), # forward
            pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/UI03.wav"), # backward
        ]

        self.ui_sound_options = {}
        self.pause_menu_options = {}
        self.event_options = {
            QUIT: lambda **kwargs: self.quit(**kwargs),
            NEXT: lambda **kwargs: self.next_music(**kwargs),
            WINDOWFOCUSGAINED: lambda **kwargs: self.window_focus(focus=False, **kwargs),
            WINDOWFOCUSLOST: lambda **kwargs: self.window_focus(focus=True, **kwargs),
            KEYDOWN: lambda **kwargs: self.key_down(**kwargs),
            MOUSEBUTTONDOWN: lambda **kwargs: self.mouse_down(**kwargs),
        }

        # Limit the type of game events that can happen
        events = []
        for event in self.event_options:
            events.append(event)
        pygame.event.set_allowed(events)

        # Game config file
        self.game_config_file_path = os.path.join(os.path.dirname(__file__), 'game_config.json')
        with open(self.game_config_file_path, encoding="utf8") as json_data_file:
            self.game_config = json.load(json_data_file)
        resolution = self.game_config["settings"]["display"]["resolution"].split("x")
        self.screen_width = int(resolution[0])
        self.screen_height = int(resolution[1])


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

            # Gameplay logic this turn/tick (dirty_rects returned)
            menu, _ = self.game.play(self.update_fps)

            # System/window events to be checked
            self.event_checks(menu, self.event_options.get)

            # Display the game screen
            pygame.display.update()

            # The game loop clocktarget FPS
            self.clock.tick(self.fps)


    def set_window_settings(self):
        '''
        set_window_settings
        ~~~~~~~~~~

        set_window_settings does stuff
        '''

        # Game window settings
        background_colour = (0, 0, 0)
        if self.game_config["settings"]["display"]["fullscreen"]:
            flags = DOUBLEBUF | FULLSCREEN
        else:
            flags = DOUBLEBUF

        # 'flags = 0' and '#, RESIZABLE)'
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags,
            16,
        )
        self.screen.set_alpha(None)
        self.debug_screen = pygame.Surface((self.screen_width, self.screen_height))
        self.debug_screen.set_colorkey((0, 0, 0))
        self.background_0 = pygame.Surface((self.screen_width, self.screen_height))
        self.background_0.set_colorkey((0, 0, 0))
        # screen.set_mode()

        alpha_screen = pygame.Surface(
            (self.screen_width, self.screen_height)
        ).convert_alpha()

        alpha_screen.fill([0,0,0,0])
        pygame.display.set_caption(self.title)
        self.screen.fill(background_colour)

        # Show game window
        pygame.display.flip()

        # Instantiate the Game Obj
        self.game = self.game_pkg(alpha_screen, self.screen, self)

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
        self.fps_pos = (self.game.screen_size[0]/2-(8*self.game.game_font.size)/2 + 535,
                        self.game.screen_size[1]/2 - self.game.game_font.size * 12,
                        250, 163)
        self.fps_rect = pygame.Rect(self.fps_pos)


    def update_fps(self):
        """AI is creating summary for update_fps

        Returns:
            [type]: [description]
        """

        # Clear previous frame obj's location
        self.debug_screen.fill((0, 0, 0), self.fps_pos)
        self.fps_pos = (self.game.screen_size[0]/2-(8*self.game.game_font.size)/2 + 535,
                        self.game.screen_size[1]/2 - self.game.game_font.size * 12,
                        250, 163)
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.fps_pos)
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
            #   QUIT, NEXT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST, KEYDOWN, MOUSEBUTTONDOWN
            decision_func = event_get(event.type)
            if decision_func:
                decision_func(event=event, menu=menu)


    def quit(self, **_):
        """AI is creating summary for quit
        """

        self.running = False


    def window_focus(self, focus, **_):
        """AI is creating summary for window_focus

        Args:
            focus ([type]): [description]
        """

        self.game.focus_pause = focus


    def window_resize(self, **kwargs):
        """AI is creating summary for window_resize
        """

        pass


    def key_down(self, **kwargs):
        """AI is creating summary for key_down
        """

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
        """AI is creating summary for mouse_down
        """

        if kwargs["menu"]:
            for button in kwargs["menu"]:
                if button[0].collidepoint(kwargs["event"].pos):
                    self.play_menu_sound(button)
                    self.game.menu.prev_menu = button[2]
                    button[1]()


    def next_music(self, **_):
        """AI is creating summary for next_music
        """

        # If not game over
        if self.game.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            pygame.mixer.music.load(self.game.playlist[self.game.current_track])
            pygame.mixer.music.play(0, 0, 1)


    def play_menu_sound(self, button):
        """AI is creating summary for play_menu_sound

        Args:
            button ([type]): [description]
        """
        num = self.ui_sound_options.get(button[1], 0)
        self.play_ui_sound(num)


    def play_ui_sound(self, num):
        """AI is creating summary for play_ui_sound

        Args:
            num ([type]): [description]
        """
        menu_sound = self.menu_sounds[num]
        menu_sound.set_volume(float(self.game_config["settings"]["sound"]["menu_volume"])/1.5)
        pygame.mixer.Sound.play(menu_sound)
