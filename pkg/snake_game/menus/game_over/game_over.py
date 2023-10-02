#!/usr/bin/env python3

"""
    Game Over Menu

    The menu screen that is shown when the game is over

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from pygame import mixer

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_GAME_OVER,
)


def game_over_menu(self):
    """game_over_menu

    game_over_menu does stuff
    """

    # Clear previous frame render
    self.app.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_GAME_OVER

    # Stop the music
    if self.app.is_audio:
        mixer.music.stop()

    # Render the Game Over text
    _ = self.render_button("Game Over", 10, color=COLOR_RED)

    # Get the player score
    score = 0
    for _, value in self.app.game.entity_final_scores.items():
        if value["is_player"]:
            score = value["score"]
            new_score = False
            # Save the score
            if self.app.game.leaderboard["highscore"] < score:
                self.app.game.leaderboard["highscore"] = score
                new_score = True

            index = 0
            for top_ten_score in self.app.game.leaderboard["top_ten"]:
                if not top_ten_score:
                    self.app.game.leaderboard["top_ten"] = [score]
                if top_ten_score < score:
                    self.app.game.leaderboard["top_ten"][index] = score
                    new_score = True
                    break

            if new_score:
                self.save_leaderboard()

    # Render the score
    _ = self.render_button('Score: ' + str(score), 8, color=COLOR_RED)

    # Render the restart button
    restart_obj = self.render_button("Restart", 1)

    # Render the quit button
    return_obj = self.render_button("Quit", -2)

    menu = [
        (restart_obj, self.app.game.start, 3),
        (return_obj, self.home_menu, 3),
    ]

    return menu
