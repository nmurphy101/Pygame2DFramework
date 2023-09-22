#!/usr/bin/env python3

"""
    Game App


    Base for a game in a window
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import os
import logging
import statistics
import json

import pygame
from pygame import (
    init, mixer, DOUBLEBUF, FULLSCREEN
)
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, MOUSEBUTTONDOWN,
    WINDOWFOCUSGAINED, WINDOWFOCUSLOST, USEREVENT
)
from guppy import hpy

from .constants import app_constants as constants


NEXT = USEREVENT + 1


def _get_log_level(json_config: dict):
    """_get_log_level

    Base game structure.
    """
    match (json_config["settings"]["debug"]["log_level"]).lower():
        case "info":
            return logging.INFO

        case "debug":
            return logging.DEBUG

        case "warning":
            return logging.WARNING

        case _:
            return logging.INFO


class App():
    """Game

    Base game structure.
    """

    def __init__(self, game_pkg):
        # setup mixer to avoid sound lag
        mixer.pre_init(44100, -16, 2, 2048)
        init()
        mixer.quit()
        mixer.init(44100, -16, 2, 2048)

        # App config file
        self.app_config_file_path = os.path.join(os.path.dirname(__file__), constants.CONFIG_FILE_NAME)
        with open(self.app_config_file_path, encoding="utf8") as json_data_file:
            self.app_config = json.load(json_data_file)

        # Setup the app logger for event tracking and debugging
        if self.app_config["settings"]["debug"]["log_level"]:
            logging.basicConfig(level=_get_log_level(self.app_config), filename=constants.LOG_FILE_NAME, filemode="w", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.debug("App started")

        # Set initial app settings
        resolution = self.app_config["settings"]["display"]["resolution"].split("x")
        self.screen_width = int(resolution[0])
        self.screen_height = int(resolution[1])
        self.game_pkg = game_pkg
        self.game = None
        self.running = True
        self.fps = self.app_config["settings"]["display"]["fps"]
        self.fps_list = []
        self.clock = None
        self.title = self.app_config["settings"]["display"]["window_title"]
        self.screen = None
        self.debug_screen = None
        self.background_0 = None

        self.menu_sounds = [
            pygame.mixer.Sound(constants.SOUND_UI_HOVER), # hover
            pygame.mixer.Sound(constants.SOUND_UI_FORWARD), # forward
            pygame.mixer.Sound(constants.SOUND_UI_BACKWARD), # backward
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


    def run(self):
        """
        run


        run does stuff
        """

        # h=hpy()

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

            # The game loop FPS counter
            is_fps_display_shown = self.app_config["settings"]["display"]["fps_display"]
            if is_fps_display_shown:
                self.fps_counter_display()

            # System/window events to be checked
            self.event_checks(menu, self.event_options.get)
            pygame.event.clear()

            # Display the game screen
            pygame.display.flip()

            # The game loop clocktarget FPS
            self.clock.tick(self.fps)

        # print(h.heap())


    def set_window_settings(self):
        """
        set_window_settings


        set_window_settings does stuff
        """

        # Game window settings
        background_colour = (0, 0, 0)
        if self.app_config["settings"]["display"]["fullscreen"]:
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


    def fps_counter_display(self):
        """fps_counter_display

        Returns:
            [type]: [description]
        """

        # _ = self.menu.render_button(f"Score:{score}", .35, -1, color=COLOR_RED, relative_from="top")

        # # Clear previous frame obj's location
        # fps_pos = (self.game.screen_size[0]/2-(8*self.game.game_font.size)/2 + 535,
        #                 self.game.screen_size[1]/2 - self.game.game_font.size * 12 + 30,
        #                 250, 135)

        # self.debug_screen.fill((128, 0, 128), fps_pos)

        # pygame.draw.rect(self.game.screen, (128, 0, 128), fps_pos)

        fps = str(int(self.clock.get_fps()))

        _ = self.game.menu.render_button(f"now:{fps}", 1.6, 4, relative_from="top")

        self.fps_list.append(int(fps))

        # Keep the fps list limited to 100 most recient samples
        if len(self.fps_list) > 200:
            self.fps_list.pop(0)

        # Average FPS
        avg_fps = str(round(statistics.mean(self.fps_list)))
        _ = self.game.menu.render_button(f"avg:{avg_fps}", 2.6, 4, relative_from="top")

        # High and low FPS
        _ = self.game.menu.render_button(f"H:{max(self.fps_list)}", 3.7, 6.45, relative_from="top")
        _ = self.game.menu.render_button(f"L:{min(self.fps_list)}", 4.7, 6.45, relative_from="top")


    def event_checks(self, menu, event_get):
        """
        event_checks


        event_checks for the game
        """

        for event in pygame.event.get():
            # Possible event options:
            #   QUIT, NEXT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST, KEYDOWN, MOUSEBUTTONDOWN
            decision_func = event_get(event.type)
            if decision_func:
                decision_func(event=event, menu=menu)


    def quit(self, **_):
        """quit
        """

        self.running = False


    def window_focus(self, focus, **_):
        """window_focus

        Args:
            focus ([type]): [description]
        """

        self.game.focus_pause = focus


    def window_resize(self, **kwargs):
        """window_resize
        """

        pass


    def key_down(self, **kwargs):
        """key_down
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
        """mouse_down
        """

        if kwargs["menu"]:
            for button in kwargs["menu"]:
                if button[0].collidepoint(kwargs["event"].pos):
                    self.play_menu_sound(button)
                    self.game.menu.prev_menu = button[2]
                    button[1]()


    def next_music(self, **_):
        """next_music
        """

        # If not game over
        if self.game.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            pygame.mixer.music.load(self.game.playlist[self.game.current_track])
            pygame.mixer.music.play(0, 0, 1)


    def play_menu_sound(self, button):
        """play_menu_sound

        Args:
            button ([type]): [description]
        """

        num = self.ui_sound_options.get(button[1], 0)
        self.play_ui_sound(num)


    def play_ui_sound(self, num):
        """play_ui_sound

        Args:
            num ([type]): [description]
        """

        menu_sound = self.menu_sounds[num]
        menu_sound.set_volume(float(self.app_config["settings"]["sound"]["menu_volume"])/1.5)
        pygame.mixer.Sound.play(menu_sound)
