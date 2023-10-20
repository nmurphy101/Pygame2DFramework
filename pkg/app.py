#!/usr/bin/env python3

"""
    Game App


    Base for a game in a window
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from inspect import currentframe, getframeinfo
from json import dump as json_dump, load as json_load
from logging import (
    INFO,
    DEBUG,
    WARNING,
    basicConfig,
    debug as logging_debug,
    info as logging_info,
)
from os import path, getcwd
from pathlib import Path
from statistics import mean

from guppy import hpy
from pygame import (
    draw as pygame_draw,
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
    USEREVENT,
)
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN,
    MOUSEBUTTONUP, WINDOWFOCUSGAINED, WINDOWFOCUSLOST, USEREVENT
)

from .constants.app_constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    CONFIG_APP_FILE_NAME,
    DEFAULT_APP_CONFIG,
    LOG_FILE_NAME,
    MENU_PAUSE,
    MOUSE_DOWN_MAP,
    REGULAR_FONT,
    REGULAR_FONT_SIZE,
    SOUND_UI_HOVER,
    SOUND_UI_FORWARD,
    SOUND_UI_BACKWARD,
)
from .menus.menus import Menu
from .app_config import AppConfig


# Define custom events
NEXT = USEREVENT + 1
MOUSEHOVER = USEREVENT + 2


def _get_log_level(json_config: AppConfig):
    """_get_log_level

    Base game structure.
    """

    match json_config["settings"]["debug"]["log_level"].lower():
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

    def __init__(self, game_list: list):
        print("Initilizing App Started")

        print("Loading pygame and audio mixer: Working", end="\r")
        # setup mixer to avoid sound lag
        self.set_up_audio_mixer()
        print("Loading pygame and audio mixer: Finished")

        # Menu settings
        self.menu = Menu(self)
        self.pause_menu_options = {}

        # App fonts
        self.app_font = freetype.Font(
            file=REGULAR_FONT,
            size=REGULAR_FONT_SIZE,
        )

        # Initial app window settings
        self.screen = pygame_display.set_mode(
            (640, 360),
            DOUBLEBUF,
            16,
        )

        self.screen.fill(COLOR_BLACK)

        text_str = "Loading. . ."
        horizontal_position = -1
        h_offset = 0
        w_offset = 0
        position = (
            640 / 2 + (len(text_str) * self.app_font.size) / 2 * horizontal_position + h_offset,
            0 + self.app_font.size * 2 + w_offset
        )
        _ = self.app_font.render_to(
            self.screen,
            position,
            text_str,
            COLOR_RED
        )

        # Show Loading screen
        pygame_display.flip()

        print("Loading app config: Working", end="\r")
        # App config file
        self.app_config_file_path = path.join(path.dirname(__file__), CONFIG_APP_FILE_NAME)
        print(path.dirname(__file__), self.app_config_file_path)
        try:
            with open(self.app_config_file_path, encoding="utf8") as json_data_file:
                self.app_config: AppConfig = json_load(json_data_file)
        except Exception as e:
            print(f"Error: {e}")
            self.app_config = DEFAULT_APP_CONFIG
            Path(path.dirname(__file__)).mkdir(parents=True, exist_ok=True)
            with open(self.app_config_file_path, "w+", encoding="utf8") as _file:
                json_dump(self.app_config, _file, ensure_ascii=False, indent=4)

        print("Loading app config: Finished")

        print("Loading logger: Working", end="\r")
        # Setup the app logger for event tracking and debugging
        if self.app_config["settings"]["debug"]["log_level"]:
            try:
                basicConfig(level=_get_log_level(self.app_config), filename=f"{getcwd()}/logs/{LOG_FILE_NAME}", filemode="w", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            except Exception as e:
                print(f"Error: {e}")
                Path(f"{getcwd()}/logs/").mkdir(parents=True, exist_ok=True)
                with open(f"{getcwd()}/logs/{LOG_FILE_NAME}", "w+", encoding="utf8"): pass
                basicConfig(level=_get_log_level(self.app_config), filename=f"{getcwd()}/logs/{LOG_FILE_NAME}", filemode="w", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        print("Loading logger: Finished")

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
        self.alpha_screen = None
        self.background_0 = None
        self.keybinding_switch = (False, None)
        self.focus_pause = False

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



        # Event settings
        self.event_options = {
            QUIT: lambda **kwargs: self.quit(**kwargs),
            NEXT: lambda **kwargs: self.next_music(**kwargs),
            WINDOWFOCUSGAINED: lambda **kwargs: self.window_focus(focus=False, **kwargs),
            WINDOWFOCUSLOST: lambda **kwargs: self.window_focus(focus=True, **kwargs),
            KEYDOWN: lambda **kwargs: self.key_down(**kwargs),
            MOUSEBUTTONDOWN: lambda **kwargs: self.mouse_down(**kwargs),
            MOUSEBUTTONUP: lambda **kwargs: self.mouse_up(**kwargs),
            MOUSEHOVER: lambda **kwargs: self.mouse_hover(**kwargs),
        }

        # Limit the type of game events that can happen
        events = []
        for event in self.event_options:
            events.append(event)
        pygame_event.set_allowed(events)

        print("Initilizing App Finished")


    def run(self):
        """
        run

        run does stuff
        """

        # h=hpy()

        # Game loop clock
        self.clock = pygame_time.Clock()

        # Game window settings
        self.set_window_settings()

        # Choose game to play
        self.choose_game_loop()

        # App loop
        while self.running:
            # Send event NEXT every time music tracks ends
            mixer.music.set_endevent(NEXT)

            chosen_menu = None
            # Go into gameplay loop if not in a menu
            if self.menu.menu_option is None:
                # Clear previous frame render
                # self.game.screen.fill(COLOR_BLACK)

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


    def set_window_settings(self) -> None:
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

        self.alpha_screen = Surface(
            (self.screen_width, self.screen_height)
        ).convert_alpha()

        self.alpha_screen.fill([0,0,0,0])
        pygame_display.set_caption(self.title)
        self.screen.fill(background_colour)

        # Show game window
        pygame_display.flip()


    def set_game_settings(self) -> None:
        # Instantiate the Game Obj
        self.game = self.game_pkg(self, self.alpha_screen, self.screen)

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


    def fps_counter_display(self) -> None:
        """fps_counter_display

        fps_counter_display for the game
        """

        fps = str(int(self.clock.get_fps()))[0:3].rjust(3, "0")

        _ = self.menu.render_text(f"now:{fps}", 1.6, 12.2, relative_from="right")

        self.fps_list.append(int(fps))

        # Keep the fps list limited to 100 most recient samples
        if len(self.fps_list) > 200:
            self.fps_list.pop(0)

        # Average FPS
        avg_fps = str(round(mean(self.fps_list)))[0:3].rjust(3, "0")
        _ = self.menu.render_text(f"avg:{avg_fps}", 2.6, 12.2, relative_from="right")

        # High and low FPS
        high_fps = str(max(self.fps_list)).rjust(3, "0")
        low_fps = str(min(self.fps_list)).rjust(3, "0")
        self.menu.render_text(f"H:{high_fps}", 3.7, 9, relative_from="right")
        self.menu.render_text(f"L:{low_fps}", 4.7, 8.8, relative_from="right")


    def event_checks(self, current_menu: int) -> None:
        """
        event_checks

        Args:
            current_menu ([type]): [description]
        """

        for event in pygame_event.get():
            # Possible event options:
            #   QUIT, NEXT, WINDOWFOCUSGAINED, WINDOWFOCUSLOST, KEYDOWN, MOUSEBUTTONDOWN
            decision_func = self.event_options.get(event.type)
            if decision_func:
                decision_func(event=event, menu=current_menu)


    def settings_checks(self) -> None:
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


    def quit(self, **_) -> None:
        """quit

        quit does stuff
        """

        self.running = False


    def window_focus(self, focus, **_) -> None:
        """window_focus

        Args:
            focus ([type]): [description]
        """

        self.focus_pause = focus


    def window_resize(self, **kwargs) -> None:
        """window_resize

        Args:
            kwargs ([args]): [description]
        """

        pass


    def change_keybinding(self, action: str, new_key: str) -> None:
        """
        change_keybinding

        Args:
            action ([str]): [description]
            new_key ([str]): [description]
        """

        # print("changing keybinding for/new_key", action, new_key)
        self.game.game_config["settings"]["keybindings"][action] = new_key.upper()
        self.menu.refresh = True


    def key_down(self, **kwargs) -> None:
        """key_down

        Args:
            kwargs ([args]): [description]
        """

        # Pressed escape to pause/unpause/back
        if kwargs["event"].key == K_ESCAPE and self.game:
            # print(self.menu.menu_option)
            if self.menu.menu_option == None:
                self.play_ui_sound(1)

                # Clear previous frame render
                self.screen.fill(COLOR_BLACK)

                # Either unpause or pause the game
                self.menu.prev_menu = self.menu.menu_option
                self.menu.menu_option = self.pause_menu_options.get(self.menu.menu_option, self.menu.prev_menu)

            elif self.menu.menu_option == MENU_PAUSE:
                self.play_menu_sound(2)
                self.game.unpause()

        elif self.keybinding_switch[0]:
            self.change_keybinding(self.keybinding_switch[1], kwargs["event"].unicode)
            self.keybinding_switch = (False, None)


    def mouse_down(self, **kwargs) -> None:
        """mouse_down

        Args:
            kwargs ([args]): [description]
        """

        if kwargs["menu"] and MOUSE_DOWN_MAP[kwargs["event"].button] == "left":
            # print("mouse down")
            for button in kwargs["menu"]:
                button_obj, _, _, _ = button
                if self.game:
                    # do some button modification to indicate you're clicking it here
                    pass


    def mouse_up(self, **kwargs) -> None:
        """mouse_up

        Args:
            kwargs ([args]): [description]
        """
        if kwargs["menu"] and MOUSE_DOWN_MAP[kwargs["event"].button] == "left":
            for button in kwargs["menu"]:
                button_obj, button_action, button_prev_menu, button_action_param = button
                if self.game:
                    pygame_draw.rect(self.alpha_screen, (255, 255, 255, 0), button_obj, 0)
                frameinfo = getframeinfo(currentframe())
                logging_debug(f"{frameinfo.filename}::{getframeinfo(currentframe()).lineno}: INFO: Testing buttons: {button}, {kwargs['event'].pos}, {kwargs['event']}")
                if button_obj.collidepoint(kwargs["event"].pos):
                    logging_debug(f"{frameinfo.filename}::{getframeinfo(currentframe()).lineno}: DEBUG: Chosen button: {button}")
                    self.play_menu_sound(button_action)

                    if self.game:
                        self.menu.prev_menu = button_prev_menu

                    button_action(button_action_param) if button_action_param else button_action()


    def mouse_hover(self, **kwargs) -> None:
        """mouse_hover

        Args:
            kwargs ([args]): [description]
        """

        # do some button modification to indicate you're hovering it here
        # possibly send an event in some other function that checks for mouse + button collision
        pass


    def next_music(self, **_) -> None:
        """next_music

        next_music does stuff
        """

        # If not game over
        if self.menu.menu_option != 3:
            # Get next track (modulo number of tracks)
            self.game.current_track = (self.game.current_track + 1) % len(self.game.playlist)
            if self.is_audio:
                mixer.music.load(self.game.playlist[self.game.current_track])
                mixer.music.play(0, 0, 1)


    def play_menu_sound(self, action) -> None:
        """play_menu_sound

        Args:
            button ([list]): [description]
        """

        num = self.ui_sound_options.get(action, 0)
        # print(f"Sound num: {num}")
        self.play_ui_sound(num)


    def play_ui_sound(self, num: int) -> None:
        """play_ui_sound

        Args:
            num ([int]): [description]
        """

        menu_sound = self.menu_sounds[num]
        if self.is_audio:
            menu_sound.set_volume(float(self.app_config["settings"]["sound"]["menu_volume"])/1.5)
            mixer.Sound.play(menu_sound)


    def choose_game_loop(self) -> None:
        """
        choose_game_loop

        choose_game_loop does stuff
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
        if self.game_pkg:
            self.set_game_settings()


    def _choose_game(self) -> list:
        """
        _choose_game

        _choose_game does stuff
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


    def _load_game(self, game_pkg: type) -> None:
        """
        _load_game

        Args:
            game_pkg ([type]): [description]
        """

        frameinfo = getframeinfo(currentframe())

        logging_info(f"{frameinfo.filename}::{getframeinfo(currentframe()).lineno}: INFO: Game Chosen: {game_pkg}")

        self.game_pkg = game_pkg
