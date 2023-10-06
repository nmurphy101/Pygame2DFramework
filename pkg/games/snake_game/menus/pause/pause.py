#!/usr/bin/env python3

"""
    Pause Menu

    Pause menu shown when the game is paused

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from gc import collect as gc_collect

from .....menus import Menu

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_HOME,
    MENU_PAUSE,
    MENU_SETTINGS,
)


def pause_menu(self: Menu):
    """pause_menu

    pause_menu does stuff
    """

    # Clear previous frame render
    self.app.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_PAUSE
    self.root_menu = MENU_PAUSE

    if self.prev_menu is None:
        # Free unreferenced memory
        gc_collect()
        self.prev_menu = MENU_SETTINGS

    # Pause game music
    self.app.pause_game_music = True

    # Render the paused text
    _ = self.render_button("-Paused-", 10, color=COLOR_RED)

    # Get the player score
    score = 0
    for obj in self.app.game.sprite_group.sprites():
        if obj.is_player:
            score = obj.score

    # Render the score
    _ = self.render_button("Score: " + str(score), 8, color=COLOR_RED)

    # Render the quit button
    resume_obj = self.render_button("Resume", 1)

    # Render the settings button
    settings_obj = self.render_button("Settings", -1)

    # Render the main menu button
    return_obj = self.render_button("Main Menu", -3)

    menu = [
        (resume_obj, self.app.game.unpause, 1),
        (settings_obj, self.menu_options[MENU_SETTINGS], 1),
        (return_obj, self.menu_options[MENU_HOME], 1),
    ]

    return menu
