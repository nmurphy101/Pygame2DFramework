#!/usr/bin/env python3

"""
    Game Over Menu

    The menu screen that is shown when the game is over

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import pygame

from ...constants import game_constants


def game_over(self):
    """game_over_menu

    game_over_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = game_constants.MENU_GAME_OVER

    # Stop the music
    pygame.mixer.music.stop()

    # Render the Game Over text
    _ = self.render_button("Game Over", 10, (255, 0, 0))

    # Get the player score
    score = "NA"
    for entity, value in self.game.entity_final_scores.items():
        if value["is_player"]:
            score = value["score"]

    # Render the score
    _ = self.render_button('Score: ' + str(score), 8, (255, 0, 0))

    # Render the restart button
    restart_obj = self.render_button("Restart", 1)

    # Render the quit button
    return_obj = self.render_button("Quit", -2)

    menu = [
        (restart_obj, self.game.start, 3),
        (return_obj, self.home_menu, 3),
    ]

    return menu
