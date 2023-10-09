#!/usr/bin/env python3

"""
    Sound Menu

    Sound settings menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from typing import TYPE_CHECKING

from ...constants.app_constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_PURPLE,
    MENU_SETTINGS,
    MENU_SOUND,
)

if TYPE_CHECKING:
    from ..menus import Menu


def sound_menu(self: "Menu"):
    """sound_menu

    sound_menu does stuff
    """

    if self.refresh or self.menu_option != MENU_SOUND:
        # Clear previous frame render
        self.app.game.screen.fill(COLOR_BLACK)

        # Make sure the right menu option is selected
        self.menu_option = MENU_SOUND

        # Render the Display text
        self.render_button("Sound", 10, color=COLOR_RED)

        # Render the music button
        _ = self.render_button('Music:', 7, h_offset=-100)
        text_str = str(self.app.app_config["settings"]["sound"]["music"])
        music_obj = self.render_button(text_str, 7, color=COLOR_PURPLE, h_offset=100, has_outline=True)

        # Render the Volume view button
        volume_num = round(
            100 * float(self.app.app_config["settings"]["sound"]["music_volume"]),
            2,
        )
        text_str = "Music Volume: " + str(volume_num)
        _ = self.render_button(text_str, 5)

        # Render the Volume Up button
        music_volume_up_obj = self.render_button("Up", 4, color=COLOR_PURPLE, w_offset=10, h_offset=100, has_outline=True)

        # Render the Volume Down button
        music_volume_down_obj = self.render_button("Down", 4, color=COLOR_PURPLE, w_offset=10, h_offset=-100, has_outline=True)

        # Render the Volume view button
        volume_num = round(
            100 * float(self.app.app_config["settings"]["sound"]["effect_volume"]),
            2,
        )
        text_str = "Effect Volume: " + str(volume_num)
        _ = self.render_button(text_str, 2)

        # Render the Volume Up button
        effect_volume_up_obj = self.render_button("Up", 1, color=COLOR_PURPLE, w_offset=10, h_offset=100, has_outline=True)

        # Render the Volume Down button
        effect_volume_down_obj = self.render_button("Down", 1, color=COLOR_PURPLE, w_offset=10, h_offset=-100, has_outline=True)

        # Render the Volume view button
        volume_num = round(100 * float(self.app.app_config["settings"]["sound"]["menu_volume"]))
        text_str = "Menu Volume: " + str(volume_num)
        _ = self.render_button(text_str, -1)

        # Render the Volume Up button
        menu_volume_up_obj = self.render_button("Up", -2, color=COLOR_PURPLE, w_offset=10, h_offset=100, has_outline=True)

        # Render the Volume Down button
        menu_volume_down_obj = self.render_button("Down", -2, color=COLOR_PURPLE, w_offset=10, h_offset=-100, has_outline=True)

        # Render the Save button
        save_obj = self.render_button("Save", -8, h_offset=125, has_outline=True)

        # Render the Return button
        back_obj = self.render_button("Back", -8, h_offset=-125, has_outline=True)

        def sound_save():
            self.save_settings()
            self.app.settings_checks()

        self.menu = [
            (music_obj, self.toggle_game_music, MENU_SOUND, None),
            (music_volume_up_obj, self.increase_music_volume, MENU_SOUND, None),
            (music_volume_down_obj, self.decrease_music_volume, MENU_SOUND, None),
            (effect_volume_up_obj, self.increase_effect_volume, MENU_SOUND, None),
            (effect_volume_down_obj, self.decrease_effect_volume, MENU_SOUND, None),
            (menu_volume_up_obj, self.increase_menu_volume, MENU_SOUND, None),
            (menu_volume_down_obj, self.decrease_menu_volume, MENU_SOUND, None),
            (save_obj, sound_save, MENU_SOUND, None),
            (back_obj, self.menu_options[MENU_SETTINGS], MENU_SOUND, None),
        ]

        self.refresh = False

    return self.menu
