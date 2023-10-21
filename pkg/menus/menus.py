#!/usr/bin/env python3

"""
    Entities

    All the entities in the game

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from json import dump as json_dump, load as json_load
from os import path
from typing import TYPE_CHECKING

from pygame import (
    mixer,
    display,
    Surface,
    transform,
    gfxdraw,
    DOUBLEBUF,
    FULLSCREEN,
    Rect,
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
        self.prev_menu = None
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

        # The chosen menu obj
        self.menu = None

        # If the menu display needs to be updated
        self.refresh = False


    def _draw_rect_outline(self, rect: Rect, color: tuple, width=1) -> None:
        """_draw_rect_outline

        Args:
            rect ([type]): [description]
            color (tuple): [description]. Defaults to WHITE.
            width (int, optional): [description]. Defaults to 1.

        """

        x, y, w, h = rect
        # Draw at least one rect.
        width = max(width, 1)

        # Don't overdraw.
        width = min(min(width, w//2), h//2)

        # This draws several smaller outlines inside the first outline. Invert
        # the direction if it should grow outwards.
        for i in range(width):
            gfxdraw.rectangle(self.app.game.screen, (x + i, y + i, w - i * 2, h - i * 2), color)


    def render_button(
        self,
        content: str,
        virtical_position: int = 1,
        horizontal_position: int = 1,
        color: tuple = COLOR_WHITE,
        relative_from: str = "center",
        clear_background: bool = True,
        h_offset: int = 0,
        w_offset: int = 0,
        screen = None,
        has_outline: bool = False,
    ) -> Rect:
        """render_button

        Args:
            content ([type]): [description]
            virtical_position ([type]): [description]
            color (tuple, optional): [description]. Defaults to WHITE.
            h_offset (int, optional): [description]. Defaults to 0.
            screen ([type], optional): [description]. Defaults to None.

        Returns:
            [Rect]: [description]
        """

        if screen:
            chosen_screen = screen

        else:
            chosen_screen = self.app.game.screen

        content = str(content)

        if relative_from == "center":
            position = (
                self.app.game.screen_size[WIDTH] / 2 - (len((content)) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.screen_size[HEIGHT] / 2 - self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "left":
            position = (
                (len((content)) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "right":
            position = (
                self.app.game.screen_size[WIDTH] - 20 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "top":
            position = (
                self.app.game.screen_size[WIDTH] / 2 + (len(content) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        # clear out first
        if clear_background:
            chosen_screen.fill(COLOR_BLACK, (position[X], position[Y], (len(content) * self.app.game.game_font.size), self.app.game.game_font.size))

        obj: Rect = self.app.game.game_font.render_to(
            chosen_screen,
            position,
            content,
            color
        )

        if has_outline:
            outline_offset = 10
            rect_pos = (position[X] - outline_offset, position[Y] - outline_offset, (len(content) * self.app.game.game_font.size) + outline_offset * 1.5, self.app.game.game_font.size + outline_offset * 1.5)
            self._draw_rect_outline(rect_pos, COLOR_WHITE)
            obj.update(rect_pos)

        return obj


    def render_text(
        self,
        content: str,
        virtical_position: int = 1,
        horizontal_position: int = 1,
        color: tuple = COLOR_WHITE,
        relative_from: str = "center",
        clear_background: bool = True,
        h_offset: int = 0,
        w_offset: int = 0,
        screen = None,
    ) -> None:
        """render_text

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

        content = str(content)

        if relative_from == "center":
            position = (
                self.app.game.screen_size[WIDTH] / 2 - (len(content) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.screen_size[HEIGHT] / 2 - self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "left":
            position = (
                (len(content) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "right":
            position = (
                self.app.game.screen_size[WIDTH] - 20 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        elif relative_from == "top":
            position = (
                self.app.game.screen_size[WIDTH] / 2 + (len(content) * self.app.game.game_font.size) / 2 * horizontal_position + h_offset,
                self.app.game.game_font.size * virtical_position + w_offset
            )

        # clear out first
        if clear_background:
            chosen_screen.fill(COLOR_BLACK, (position[X], position[Y], (len(content) * self.app.game.game_font.size), self.app.game.game_font.size))

        self.app.game.game_font.render_to(
            chosen_screen,
            position,
            content,
            color
        )


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

        if self.app.is_audio:
            music_volume = self.app.app_config["settings"]["sound"]["music_volume"]
            mixer.music.set_volume(float(music_volume))


    def save_leaderboard(self):
        """save_leaderboard

        save_leaderboard does stuff
        """

        with open(self.app.game.leaderboard_file_path, "w", encoding="utf-8") as _file:
            json_dump(self.app.game.leaderboard, _file, ensure_ascii=False, indent=4)


    def reload_settings(self):
        """save_leaderboard

        save_leaderboard does stuff
        """

        # App config file
        with open(self.app.app_config_file_path, encoding="utf8") as json_data_file:
            self.app.app_config = json_load(json_data_file)

         # Game config file
        with open(self.app.game.game_config_file_path, encoding="utf8") as json_data_file:
            self.app.game.game_config = json_load(json_data_file)


    def toggle_setting(self, config, page, setting_name):
       config["settings"][page][setting_name] = not config["settings"][page][setting_name]
       self.refresh = True


    def toggle_game_music(self):
        """ toggle_game_music

        toggle_game_music does stuff
        """

        self.toggle_setting(self.app.app_config, "sound", "music")
        self.refresh = True


    def increase_music_volume(self):
        """ increase_music_volume

        increase_music_volume does stuff
        """

        music_volume = self.app.app_config["settings"]["sound"]["music_volume"]
        self.app.app_config["settings"]["sound"]["music_volume"] = round(float(music_volume) + .05, 2)
        self.refresh = True


    def decrease_music_volume(self):
        """ decrease_music_volume

        decrease_music_volume does stuff
        """

        music_volume = self.app.app_config["settings"]["sound"]["music_volume"]
        self.app.app_config["settings"]["sound"]["music_volume"] = round(float(music_volume) - .05, 2)
        self.refresh = True


    def increase_effect_volume(self):
        """ increase_effect_volume

        increase_effect_volume does stuff
        """

        effect_volume = self.app.app_config["settings"]["sound"]["effect_volume"]
        self.app.app_config["settings"]["sound"]["effect_volume"] = round(float(effect_volume) + .05, 2)
        self.refresh = True


    def decrease_effect_volume(self):
        """ decrease_effect_volume

        decrease_effect_volume does stuff
        """

        effect_volume = self.app.app_config["settings"]["sound"]["effect_volume"]
        self.app.app_config["settings"]["sound"]["effect_volume"] = round(float(effect_volume) - .05, 2)
        self.refresh = True


    def increase_menu_volume(self):
        """ increase_menu_volume

        increase_menu_volume does stuff
        """

        menu_volume = self.app.app_config["settings"]["sound"]["menu_volume"]
        self.app.app_config["settings"]["sound"]["menu_volume"] = (
            str(float(menu_volume) + .05)
        )
        self.refresh = True


    def decrease_menu_volume(self):
        """ decrease_menu_volume

        decrease_menu_volume does stuff
        """

        menu_volume = self.app.app_config["settings"]["sound"]["menu_volume"]
        self.app.app_config["settings"]["sound"]["menu_volume"] = (
            str(float(menu_volume) - .05)
        )
        self.refresh = True


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
        self.refresh = True


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
        self.refresh = True


    def toggle_gameplay_setting(self, setting):
        """ toggle_gameplay_setting

        toggle_gameplay_setting does stuff
        """

        self.toggle_setting(self.app.game.game_config, "gameplay", setting)
        self.refresh = True


    def toggle_fps_display(self):
        """ toggle_fps_display

        toggle_fps_display does stuff
        """

        self.toggle_setting(self.app.app_config, "display", "fps_display")
        self.refresh = True


    def toggle_fullscreen(self):
        """ toggle_fullscreen

        toggle_fullscreen does stuff
        """

        self.toggle_setting(self.app.app_config, "display", "fullscreen")
        display.toggle_fullscreen()
        self.refresh = True


    def select_keybinding(self, action):
        """ select_keybinding

        select_keybinding does stuff
        """

        self.app.keybinding_switch = (True, action)
        self.app.game.game_config["settings"]["keybindings"][action] = "Select"
        self.refresh = True


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
        self.refresh = True
