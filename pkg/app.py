#!/usr/bin/env python3

"""
    Game App


    Base for a game in a window
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from inspect import currentframe, getframeinfo
from json import load as json_load
from logging import (
    INFO,
    DEBUG,
    WARNING,
    basicConfig,
    debug as logging_debug,
    info as logging_info,
)
from os import path, getcwd
from statistics import mean

from pygame import (
    event as pygame_event,
    error as pygame_error,
    display as pygame_display,
    freetype,
    init as pygame_init,
    get_init as pygame_get_init,
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
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    CONFIG_FILE_NAME,
    LOG_FILE_NAME,
    MENU_HOME,
    MENU_PAUSE,
    MENU_SETTINGS,
    MENU_GAME_OVER,
    MENU_KEYBINDING,
    MENU_GAMEPLAY,
    MOUSE_DOWN_MAP,
    REGULAR_FONT,
    REGULAR_FONT_SIZE,
    SOUND_UI_HOVER,
    SOUND_UI_FORWARD,
    SOUND_UI_BACKWARD,
)
from .menus.menus import Menu


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
        self.set_up_audio_mixer()

        # App config file
        self.app_config_file_path = path.join(path.dirname(__file__), CONFIG_FILE_NAME)
        with open(self.app_config_file_path, encoding="utf8") as json_data_file:
            self.app_config = json_load(json_data_file)

        # Setup the app logger for event tracking and debugging
        if self.app_config["settings"]["debug"]["log_level"]:
            print(f"{getcwd()}/{LOG_FILE_NAME}")
            basicConfig(level=_get_log_level(self.app_config), filename=f"{getcwd()}/logs/{LOG_FILE_NAME}", filemode="w", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

        logging_info("App started")

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

        # Sound settings
        if self.is_audio:
            self.menu_sounds = [
                mixer.Sound(SOUND_UI_HOVER), # hover
                mixer.Sound(SOUND_UI_FORWARD), # forward
                mixer.Sound(SOUND_UI_BACKWARD), # backward
            ]
        else :
            self.menu_sounds = [None, None, None]

        self.ui_sound_options = {}
        self.pause_game_music = False

        # Menu settings
        self.menu = Menu(self)
        self.pause_menu_options = {}

        # Event settings
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

        # App loop
        while self.running:
            # Send event NEXT every time music tracks ends
            if self.is_audio:
                mixer.music.set_endevent(NEXT)

            chosen_menu = None
            # Go into gameplay loop if not in a menu
            if self.menu.menu_option is None:

                # Gameplay logic/drawing this turn/tick
                self.game.play_loop()

            else:
                # Show which ever menu option that has been chosen
                chosen_menu = self.menu.menu_options.get(self.menu.menu_option)()

            # The game loop FPS counter
            is_fps_display_shown = self.app_config["settings"]["display"]["fps_display"]
            if is_fps_display_shown:
                self.fps_counter_display()

            # System/window events to be checked
            self.event_checks(chosen_menu)
            pygame_event.clear()

            # Display the game screen
            pygame_display.flip()

            # The game loop clocktarget FPS
            self.clock.tick(self.fps)

        # print(h.heap())


    def set_up_audio_mixer(self):
        """
        set_up_audio_mixer


        set_up_audio_mixer does stuff
        """

        if not pygame_get_init():
            # setup mixer to avoid sound lag
            mixer.pre_init(44100, -16, 2, 2048)
            pygame_init()
            mixer.quit()
            self.is_audio = False
            try:
                mixer.init(44100, -16, 2, 2048)
                self.is_audio = True
            except pygame_error:
                pass

        else:
            # setup mixer to avoid sound lag
            mixer.pre_init(44100, -16, 2, 2048)
            mixer.quit()
            self.is_audio = False
            try:
                mixer.init(44100, -16, 2, 2048)
                self.is_audio = True
            except pygame_error:
                pass


    def set_window_settings(self):
        """
        set_window_settings


        set_window_settings does stuff
        """

        # Game window settings
        background_colour = COLOR_BLACK
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
        self.debug_screen.set_colorkey(COLOR_BLACK)
        self.background_0 = Surface((self.screen_width, self.screen_height))
        self.background_0.set_colorkey(COLOR_BLACK)

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
            0: self.menu.menu_option,
            1: None,
            None: 1,
        }


    def fps_counter_display(self):
        """fps_counter_display

        Returns:
            [type]: [description]
        """

        fps = str(int(self.clock.get_fps()))

        _ = self.menu.render_button(f"now:{fps}", 1.6, 4, relative_from="top")

        self.fps_list.append(int(fps))

        # Keep the fps list limited to 100 most recient samples
        if len(self.fps_list) > 200:
            self.fps_list.pop(0)

        # Average FPS
        avg_fps = str(round(mean(self.fps_list)))
        _ = self.menu.render_button(f"avg:{avg_fps}", 2.6, 4, relative_from="top")

        # High and low FPS
        _ = self.menu.render_button(f"H:{max(self.fps_list)}", 3.7, 6.45, relative_from="top")
        _ = self.menu.render_button(f"L:{min(self.fps_list)}", 4.7, 6.45, relative_from="top")


    def event_checks(self, current_menu):
        """
        event_checks


        event_checks for the game
        """

        for event in pygame_event.get():
            # Possible event options:
            #   QUIT, NEXT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST, KEYDOWN, MOUSEBUTTONDOWN
            decision_func = self.event_options.get(event.type)
            if decision_func:
                decision_func(event=event, menu=current_menu)


    def settings_checks(self):
        """settings_checks

        settings_checks does stuff
        """
        # Start/Restart the game music
        if self.is_audio:
            self.set_up_audio_mixer()
            is_playing = mixer.music.get_busy()
            if self.app_config["settings"]["sound"]["music"] and not is_playing:
                mixer.music.load(self.game.playlist[self.game.current_track])
                mixer.music.set_volume(
                    float(self.app_config["settings"]["sound"]["music_volume"])
                )
                mixer.music.play(0, 0, 1)

            elif not self.app_config["settings"]["sound"]["music"] and is_playing:
                mixer.music.pause()


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
        self.menu.save_settings()


    def key_down(self, **kwargs):
        """key_down
        """

        # Pressed escape to pause/unpause/back
        if kwargs["event"].key == K_ESCAPE and self.game:
            # If not game over
            if self.menu.menu_option != 3:
                self.play_ui_sound(1)

                # Clear previous frame render
                self.screen.fill(COLOR_BLACK)

                # Either unpause or pause the game
                self.menu.prev_menu = self.menu.menu_option
                self.menu.menu_option = self.pause_menu_options.get(self.menu.menu_option, self.menu.prev_menu)

        elif self.keybinding_switch[0]:
            self.change_keybinding(self.keybinding_switch[1], kwargs["event"].unicode)
            self.keybinding_switch = (False, None)


    def mouse_down(self, **kwargs):
        """mouse_down
        """

        if kwargs["menu"] and MOUSE_DOWN_MAP[kwargs["event"].button] == "left":
            for button in kwargs["menu"]:
                frameinfo = getframeinfo(currentframe())
                logging_debug(f"{frameinfo.filename}::{getframeinfo(currentframe()).lineno}: INFO: Testing buttons: {button}, {kwargs['event'].pos}, {kwargs['event']}")
                if button[0].collidepoint(kwargs["event"].pos):
                    logging_debug(f"{frameinfo.filename}::{getframeinfo(currentframe()).lineno}: DEBUG: Chosen button: {button}")
                    self.play_menu_sound(button)

                    if self.game:
                        self.menu.prev_menu = button[2]

                    button[1](button[3]) if len(button) == 4 else button[1]()


    def next_music(self, **_):
        """next_music
        """

        # If not game over
        if self.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            if self.is_audio:
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
        if self.is_audio:
            menu_sound.set_volume(float(self.app_config["settings"]["sound"]["menu_volume"])/1.5)
            mixer.Sound.play(menu_sound)


    def choose_game_loop(self, alpha_screen):
        """
        run

        run does stuff
        """

        # Choose Game loop
        while not self.game_pkg and self.running:
            # Send event NEXT every time music tracks ends
            if self.is_audio:
                mixer.music.set_endevent(NEXT)

            # Gameplay logic this turn/tick
            menu = self._choose_game()

            # System/window events to be checked
            self.event_checks(menu)
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

        index = 3
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
        frameinfo = getframeinfo(currentframe())
        logging_info(f"INFO: Game Chosen: {game_pkg}")
        self.game_pkg = game_pkg
