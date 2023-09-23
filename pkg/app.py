#!/usr/bin/env python3

"""
    Game App


    Base for a game in a window
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from os import path
from logging import (
    INFO, DEBUG, WARNING, basicConfig, debug as logging_debug
)
from statistics import mean
from json import load as json_load

from pygame import (
    event as pygame_event,
    display as pygame_display,
    freetype,
    init,
    time as pygame_time,
    mixer,
    Surface,
    DOUBLEBUF,
    FULLSCREEN,
)
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE, RESIZABLE, MOUSEBUTTONDOWN,
    WINDOWFOCUSGAINED, WINDOWFOCUSLOST, USEREVENT
)
from guppy import hpy

from .constants.app_constants import (
    COLOR_RED,
    COLOR_PURPLE,
    CONFIG_FILE_NAME,
    LOG_FILE_NAME,
    REGULAR_FONT,
    REGULAR_FONT_SIZE,
    SOUND_UI_HOVER,
    SOUND_UI_FORWARD,
    SOUND_UI_BACKWARD,
)


NEXT = USEREVENT + 1


def _get_log_level(json_config: dict):
    """_get_log_level

    Base game structure.
    """
    match (json_config["settings"]["debug"]["log_level"]).lower():
        case "info":
            return INFO

        case "debug":
            return DEBUG

        case "warning":
            return WARNING

        case _:
            return INFO


class App():
    """Game

    Base game structure.
    """

    def __init__(self, game_list):
        # setup mixer to avoid sound lag
        mixer.pre_init(44100, -16, 2, 2048)
        init()
        mixer.quit()
        mixer.init(44100, -16, 2, 2048)

        # App config file
        self.app_config_file_path = path.join(path.dirname(__file__), CONFIG_FILE_NAME)
        with open(self.app_config_file_path, encoding="utf8") as json_data_file:
            self.app_config = json_load(json_data_file)

        # Setup the app logger for event tracking and debugging
        if self.app_config["settings"]["debug"]["log_level"]:
            basicConfig(level=_get_log_level(self.app_config), filename=LOG_FILE_NAME, filemode="w", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging_debug("App started")

        # Set initial app settings
        resolution = self.app_config["settings"]["display"]["resolution"].split("x")
        self.screen_width = int(resolution[0])
        self.screen_height = int(resolution[1])
        self.game_list = game_list
        self.game_pkg = None
        self.game = None
        self.running = True
        self.fps = self.app_config["settings"]["display"]["fps"]
        self.fps_list = []
        self.clock = None
        self.title = self.app_config["settings"]["display"]["window_title"]
        self.screen = None
        self.debug_screen = None
        self.background_0 = None
        self.keybinding_switch = (False, None)
        self.focus_pause = False

        # App fonts
        self.app_font = freetype.Font(
            file=REGULAR_FONT,
            size=REGULAR_FONT_SIZE,
        )

        self.menu_sounds = [
            mixer.Sound(SOUND_UI_HOVER), # hover
            mixer.Sound(SOUND_UI_FORWARD), # forward
            mixer.Sound(SOUND_UI_BACKWARD), # backward
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
        pygame_event.set_allowed(events)


    def run(self):
        """
        run


        run does stuff
        """

        # h=hpy()

        # Game loop clock
        self.clock = pygame_time.Clock()

        # Game window settings
        alpha_screen = self.set_window_settings()

        # Choose game to play
        self.choose_game_loop(alpha_screen)

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
            pygame_event.clear()

            # Display the game screen
            pygame_display.flip()

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
        self.screen = pygame_display.set_mode(
            (self.screen_width, self.screen_height),
            flags,
            16,
        )
        self.screen.set_alpha(None)
        self.debug_screen = Surface((self.screen_width, self.screen_height))
        self.debug_screen.set_colorkey((0, 0, 0))
        self.background_0 = Surface((self.screen_width, self.screen_height))
        self.background_0.set_colorkey((0, 0, 0))

        alpha_screen = Surface(
            (self.screen_width, self.screen_height)
        ).convert_alpha()

        alpha_screen.fill([0,0,0,0])
        pygame_display.set_caption(self.title)
        self.screen.fill(background_colour)

        # Show game window
        pygame_display.flip()

        return alpha_screen


    def set_game_settings(self, alpha_screen):
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

        fps = str(int(self.clock.get_fps()))

        _ = self.game.menu.render_button(f"now:{fps}", 1.6, 4, relative_from="top")

        self.fps_list.append(int(fps))

        # Keep the fps list limited to 100 most recient samples
        if len(self.fps_list) > 200:
            self.fps_list.pop(0)

        # Average FPS
        avg_fps = str(round(mean(self.fps_list)))
        _ = self.game.menu.render_button(f"avg:{avg_fps}", 2.6, 4, relative_from="top")

        # High and low FPS
        _ = self.game.menu.render_button(f"H:{max(self.fps_list)}", 3.7, 6.45, relative_from="top")
        _ = self.game.menu.render_button(f"L:{min(self.fps_list)}", 4.7, 6.45, relative_from="top")


    def event_checks(self, menu, event_get):
        """
        event_checks


        event_checks for the game
        """

        for event in pygame_event.get():
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

        self.focus_pause = focus


    def window_resize(self, **kwargs):
        """window_resize
        """

        pass


    def change_keybinding(self, action, new_key):
        """
        change_keybinding

        change_keybinding does stuff
        """

        # print("changing keybinding for/new_key", action, new_key)
        self.game.game_config["settings"]["keybindings"][action] = new_key.upper()
        self.game.menu.save_settings()


    def key_down(self, **kwargs):
        """key_down
        """

        # Pressed escape to pause/unpause/back
        if kwargs["event"].key == K_ESCAPE and self.game:
            # If not game over
            if self.game.menu.menu_option != 3:
                self.play_ui_sound(1)

                # Either unpause or pause the game
                self.game.menu.prev_menu = self.game.menu.menu_option
                self.game.menu.menu_option = self.pause_menu_options.get(self.game.menu.menu_option, self.game.menu.prev_menu)

            # If game over
            else:
                self.game.start()

        elif self.keybinding_switch[0]:
            self.change_keybinding(self.keybinding_switch[1], kwargs["event"].unicode)
            self.keybinding_switch = (False, None)


    def mouse_down(self, **kwargs):
        """mouse_down
        """

        if kwargs["menu"]:
            for button in kwargs["menu"]:
                # print("testing buttons: ", button, kwargs["event"].pos, kwargs["event"])
                if button[0].collidepoint(kwargs["event"].pos):
                    # print("chosen button: ", button)
                    self.play_menu_sound(button)

                    if self.game:
                        self.game.menu.prev_menu = button[2]

                    button[1](button[3]) if len(button) == 4 else button[1]()


    def next_music(self, **_):
        """next_music
        """

        # If not game over
        if self.game.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            mixer.music.load(self.game.playlist[self.game.current_track])
            mixer.music.play(0, 0, 1)


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
        mixer.Sound.play(menu_sound)


    def choose_game_loop(self, alpha_screen):
        """
        run

        run does stuff
        """

        # Take the game to be initalized
        # snake_game = SnakeGame

        # Choose Game loop
        while not self.game_pkg and self.running:
            # Send event NEXT every time music tracks ends
            mixer.music.set_endevent(NEXT)

            # Gameplay logic this turn/tick
            menu = self._choose_game()

            # System/window events to be checked
            self.event_checks(menu, self.event_options.get)
            pygame_event.clear()

            # Display the game screen
            pygame_display.flip()

            # The game loop clocktarget FPS
            self.clock.tick(self.fps)

        # Complete final game settings
        self.set_game_settings(alpha_screen)


    def _choose_game(self):
        """
        play

        play does stuff
        """

        menu = []

        # render the choose game title
        text_str = "Choose Game"
        horizontal_position = -1
        h_offset = 0
        w_offset = 0
        position = (
            self.screen_width / 2 + (len(text_str) * self.app_font.size) / 2 * horizontal_position + h_offset,
            0 + self.app_font.size * 2 + w_offset
        )
        _ = self.app_font.render_to(
            self.screen,
            position,
            text_str,
            COLOR_RED
        )

        index = 6
        # render the game options
        for game in self.game_list:
            text_str = game.TITLE
            horizontal_position = -1
            h_offset = 0
            w_offset = 20
            position = (
                self.screen_width / 2 + (len(text_str) * self.app_font.size) / 2 * horizontal_position + h_offset,
                0 + self.app_font.size * (index*2) + w_offset
            )
            button = self.app_font.render_to(
                self.screen,
                position,
                text_str,
                COLOR_PURPLE
            )

            # print("game added: ", game)
            menu.append((button, self._load_game, 0, game))
            index += 1

        return menu


    def _load_game(self, game_pkg):
        # print("Game Chosen: ", game_pkg)
        self.game_pkg = game_pkg
