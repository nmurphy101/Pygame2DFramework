#!/usr/bin/env python3

"""
    Game Over Menu

    The menu screen that is shown when the game is over

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import pygame

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_GAME_OVER,
)


def game_over(self):
    """game_over_menu

    game_over_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_GAME_OVER

    # Stop the music
    pygame.mixer.music.stop()

    # Render the Game Over text
    _ = self.render_button("Game Over", 10, color=COLOR_RED)

    # Get the player score
    score = 0
    for _, value in self.game.entity_final_scores.items():
        if value["is_player"]:
            score = value["score"]

    # Render the score
    _ = self.render_button('Score: ' + str(score), 8, color=COLOR_RED)

    # Render the restart button
    restart_obj = self.render_button("Restart", 1)

    # Render the quit button
    return_obj = self.render_button("Quit", -2)

    menu = [
        (restart_obj, self.game.start, 3),
        (return_obj, self.home_menu, 3),
    ]

    return menu
