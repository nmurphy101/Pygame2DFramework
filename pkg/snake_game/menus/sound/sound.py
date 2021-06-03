#!/usr/bin/env python3

'''
    Sound Menu
    ~~~~~~~~~~

    Sound settings menu


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
'''

import pygame


def sound_menu(self):
    '''
    sound_menu
    ~~~~~~~~~~

    sound_menu does stuff
    '''
    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 5

    # Render the Display text
    self.render_button("Sound", 10, (255, 0, 0))

    # Render the music button
    text_str = 'Music: ' + str(self.game.app.game_config["settings"]["sound"]["music"])
    music_obj = self.render_button(text_str, 8)

    # Render the Volume view button
    volume_num = round(100 * float(self.game.app.game_config["settings"]["sound"]["music_volume"]), 2)
    text_str = "Music Volume: " + str(volume_num)
    _ = self.render_button(text_str, 6)

    # Render the Volume Up button
    music_volume_up_obj = self.render_button("Up", 5, h_offset=100)

    # Render the Volume Down button
    music_volume_down_obj = self.render_button("Down", 5, h_offset=-100)

    # Render the Volume view button
    volume_num = round(100 * float(self.game.app.game_config["settings"]["sound"]["effect_volume"]), 2)
    text_str = "Effect Volume: " + str(volume_num)
    _ = self.render_button(text_str, 4)

    # Render the Volume Up button
    effect_volume_up_obj = self.render_button("Up", 3, h_offset=100)

    # Render the Volume Down button
    effect_volume_down_obj = self.render_button("Down", 3, h_offset=-100)

    # Render the Volume view button
    volume_num = round(100 * float(self.game.app.game_config["settings"]["sound"]["menu_volume"]), 2)
    text_str = "Menu Volume: " + str(volume_num)
    _ = self.render_button(text_str, 2)

    # Render the Volume Up button
    menu_volume_up_obj = self.render_button("Up", 1, h_offset=100)

    # Render the Volume Down button
    menu_volume_down_obj = self.render_button("Down", 1, h_offset=-100)

    # Render the Return button
    back_obj = self.render_button("Back", -8)

    menu = [
        (music_obj, self.toggle_game_music, self.prev_menu),
        (music_volume_up_obj, self.increase_music_volume, self.prev_menu),
        (music_volume_down_obj, self.decrease_music_volume, self.prev_menu),
        (effect_volume_up_obj, self.increase_effect_volume, self.prev_menu),
        (effect_volume_down_obj, self.decrease_effect_volume, self.prev_menu),
        (menu_volume_up_obj, self.increase_menu_volume, self.prev_menu),
        (menu_volume_down_obj, self.decrease_menu_volume, self.prev_menu),
        (back_obj, self.SettingsMenu, 5),
    ]

    return menu
