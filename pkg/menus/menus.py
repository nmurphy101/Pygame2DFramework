#!/usr/bin/env python3

"""
    Entities

    All the entities in the game

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from json import dump as json_dump, load as json_load
from typing import TYPE_CHECKING

from pygame import (
    mixer,
    display,
    Surface,
    transform,
    DOUBLEBUF,
    FULLSCREEN,
)

from .display import display_menu
from .sound import sound_menu

from ..constants.app_constants import (
    COLOR_BLACK,
    COLOR_WHITE,
    MENU_HOME,
    MENU_PAUSE,
    MENU_SETTINGS,
    MENU_GAME_OVER,
    MENU_DISPLAY,
    MENU_SOUND,
    MENU_KEYBINDING,
    MENU_GAMEPLAY,
    MENU_LEADERBOARD,
    WIDTH,
    HEIGHT,
    X,
    Y,
)

if TYPE_CHECKING:
    from ..app import App


class Menu():
    """Menu

    All menus for the game
    """

    def __init__(self, app: "App"):
        """__init__

        Args:
            game ([type]): [description]
        """

        # Game that's calling the menus
        self.app = app

        # Game settings
        self.menu_option = MENU_HOME
        self.prev_menu = MENU_HOME
        self.root_menu = MENU_HOME

        # Menu options
        self.menu_options = {
            MENU_HOME: None, # home_menu from chosen_game
            MENU_PAUSE: None, # pause_menu from chosen_game
            MENU_SETTINGS: None, # settings_menu from chosen_game
            MENU_GAME_OVER: None, # game_over_menu from chosen_game
            MENU_DISPLAY: lambda: display_menu(self),
            MENU_SOUND: lambda: sound_menu(self),
            MENU_KEYBINDING: None, # keybinding_menu from chosen_game
            MENU_GAMEPLAY: None, # gameplay_menu from chosen_game
            MENU_LEADERBOARD: None, # leaderboard_menu from chosen_game
        }


    def render_button(
        self,
        title,
        virtical_position=1,
        horizontal_position=1,
        color=COLOR_WHITE,
        relative_from="center",
        clear_background=True,
        h_offset=0,
        w_offset=0,
        screen=None
    ):
        """render_button

        Args:
            title ([type]): [description]
            virtical_position ([type]): [description]
            color (tuple, optional): [description]. Defaults to WHITE.
            h_offset (int, optional): [description]. Defaults to 0.
            screen ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """

        if screen:
            chosen_screen = screen

        else:
            chosen_screen = self.app.game.screen

        # Render the Display text
        text_str = str(title)

        if relative_from == "center":
            position = (
                self.app.game.screen_size[WIDTH] / 2 - (len(text_str) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.screen_size[HEIGHT] / 2 - self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "left":
            position = (
                (len(text_str) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "right":
            position = (
                self.app.game.screen_size[WIDTH] - 20 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "top":
            position = (
                self.app.game.screen_size[WIDTH] / 2 + (len(text_str) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        # clear out first
        if clear_background:
            chosen_screen.fill(COLOR_BLACK, (position[X], position[Y], (len(text_str) * self.app.game.game_font.size), self.app.game.game_font.size))

        obj = self.app.game.game_font.render_to(
            chosen_screen,
            position,
            text_str,
            color
        )

        return obj


    def save_settings(self):
        """save_settings

        save_settings does stuff
        """

        # Save the app settings config
        with open(self.app.app_config_file_path, "w", encoding="utf-8") as _file:
            json_dump(self.app.app_config, _file, ensure_ascii=False, indent=4)

        # Save the game settings config
        with open(self.app.game.game_config_file_path, "w", encoding="utf-8") as _file:
            json_dump(self.app.game.game_config, _file, ensure_ascii=False, indent=4)


    def save_leaderboard(self):
        """save_leaderboard

        save_leaderboard does stuff
        """

        with open(self.app.game.leaderboard_file_path, "w", encoding="utf-8") as _file:
            json_dump(self.app.game.leaderboard, _file, ensure_ascii=False, indent=4)


    def toggle_setting(self, config, page, setting_name):
       config["settings"][page][setting_name] = not config["settings"][page][setting_name]


    def toggle_game_music(self):
        """ toggle_game_music

        toggle_game_music does stuff
        """

        self.toggle_setting(self.app.app_config, "sound", "music")


    def increase_music_volume(self):
        """ increase_music_volume

        increase_music_volume does stuff
        """

        music_volume = self.app.app_config["settings"]["sound"]["music_volume"]
        self.app.app_config["settings"]["sound"]["music_volume"] = round(str(float(music_volume) + .05), 2)
        if self.app.is_audio:
            mixer.music.set_volume(float(music_volume))


    def decrease_music_volume(self):
        """ decrease_music_volume

        decrease_music_volume does stuff
        """

        music_volume = self.app.app_config["settings"]["sound"]["music_volume"]
        self.app.app_config["settings"]["sound"]["music_volume"] = round(str(float(music_volume) - .05), 2)
        if self.app.is_audio:
            mixer.music.set_volume(float(music_volume))


    def increase_effect_volume(self):
        """ increase_effect_volume

        increase_effect_volume does stuff
        """

        effect_volume = self.app.app_config["settings"]["sound"]["effect_volume"]
        self.app.app_config["settings"]["sound"]["effect_volume"] = round(str(float(effect_volume) + .05), 2)


    def decrease_effect_volume(self):
        """ decrease_effect_volume

        decrease_effect_volume does stuff
        """

        effect_volume = self.app.app_config["settings"]["sound"]["effect_volume"]
        self.app.app_config["settings"]["sound"]["effect_volume"] = round(str(float(effect_volume) - .05), 2)


    def increase_menu_volume(self):
        """ increase_menu_volume

        increase_menu_volume does stuff
        """

        menu_volume = self.app.app_config["settings"]["sound"]["menu_volume"]
        self.app.app_config["settings"]["sound"]["menu_volume"] = (
            str(float(menu_volume) + .05)
        )


    def decrease_menu_volume(self):
        """ decrease_menu_volume

        decrease_menu_volume does stuff
        """

        menu_volume = self.app.app_config["settings"]["sound"]["menu_volume"]
        self.app.app_config["settings"]["sound"]["menu_volume"] = (
            str(float(menu_volume) - .05)
        )


    def increase_gameplay_setting(self, setting):
        """ increase_gameplay_setting

        increase_gameplay_setting does stuff
        """

        if "speed" in setting.lower():
            change_mod = 0.1
        else:
            change_mod = 1

        setting_value = self.app.game.game_config["settings"]["gameplay"][setting]
        self.app.game.game_config["settings"]["gameplay"][setting] = (
            round(setting_value + change_mod, 1)
        )


    def decrease_gameplay_setting(self, setting):
        """ decrease_gameplay_setting

        decrease_gameplay_setting does stuff
        """

        if "speed" in setting.lower():
            change_mod = 0.1
        else:
            change_mod = 1

        setting_value = self.app.game.game_config["settings"]["gameplay"][setting]
        self.app.game.game_config["settings"]["gameplay"][setting] = (
            round(setting_value - change_mod, 1)
        )


    def toggle_gameplay_setting(self, setting):
        """ toggle_gameplay_setting

        toggle_gameplay_setting does stuff
        """

        # print("toggling setting: {setting}")
        self.toggle_setting(self.app.game.game_config, "gameplay", setting)


    def toggle_fps_display(self):
        """ toggle_fps_display

        toggle_fps_display does stuff
        """

        self.toggle_setting(self.app.app_config, "display", "fps_display")


    def toggle_fullscreen(self):
        """ toggle_fullscreen

        toggle_fullscreen does stuff
        """

        self.toggle_setting(self.app.app_config, "display", "fullscreen")
        display.toggle_fullscreen()


    def change_keybinding(self, action):
        """ change_keybinding

        change_keybinding does stuff
        """

        self.app.keybinding_switch = (True, action)
        self.app.game.game_config["settings"]["keybindings"][action] = "Select"


    def change_resolution(self, resolution):
        """ change_resolution

        change_resolution does stuff
        """

        self.app.app_config["settings"]["display"]["resolution"] = resolution
        self.app.screen_width = int(resolution.split("x")[0])
        self.app.screen_height = int(resolution.split("x")[1])
        game_width = self.app.screen_width - (self.app.screen_width % self.app.game.grid_size)
        game_height = self.app.screen_height - (self.app.screen_height % self.app.game.grid_size)
        self.app.game.screen_size = (game_width, game_height)

        if self.app.app_config["settings"]["display"]["fullscreen"]:
            flags = DOUBLEBUF | FULLSCREEN
        else:
            flags = DOUBLEBUF

        # Modify all game screens with new resolution    (#, RESIZABLE))
        self.app.game.screen = display.set_mode(
            (self.app.screen_width, self.app.screen_height),
            flags,
            self.app.game.grid_size,
        )

        self.app.game.screen.set_alpha(None)

        self.app.debug_screen = Surface(
            (self.app.screen_width, self.app.screen_height)
        )

        self.app.debug_screen.set_colorkey()

        self.app.background_0 = Surface(
            (self.app.screen_width, self.app.screen_height)
        )

        self.app.background_0.set_colorkey(COLOR_BLACK)
