#!/usr/bin/env python3

"""
    Game Over Menu

    The menu screen that is shown when the game is over

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from pygame import mixer

from .....menus import Menu

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_HOME,
    MENU_GAME_OVER,
)


def game_over_menu(self: Menu):
    """game_over_menu

    game_over_menu does stuff
    """

    if self.refresh or self.menu_option != MENU_GAME_OVER:
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

        # Render the score
        _ = self.render_button('Score: ' + str(score), 8, color=COLOR_RED)

        # Render the restart button
        restart_obj = self.render_button("Restart", 1, has_outline=True)

        # Render the quit button
        quit_obj = self.render_button("Quit", -2, has_outline=True)

        def restart():
            _get_score(self)
            self.app.game.start()

        def return_to_home():
            _get_score(self)
            self.menu_options[MENU_HOME]()

        self.menu = [
            (restart_obj, restart, 3, None),
            (quit_obj, return_to_home, 3, None),
        ]

        self.refresh = False

    return self.menu




def _get_score(self):

    for _, value in self.app.game.entity_final_scores.items():
        if value["is_player"]:
            score = value["score"]
            is_new_score = False

            # Save the high-score
            if self.app.game.leaderboard["highscore"] < score:
                self.app.game.leaderboard["highscore"] = score
                is_new_score = True

            self.app.game.leaderboard["top_ten"].sort()

            # Add this score to the top_ten
            if len(self.app.game.leaderboard["top_ten"]) == 0:
                self.app.game.leaderboard["top_ten"] = [score]
                is_new_score = True

            elif len(self.app.game.leaderboard["top_ten"]) < 10:
                self.app.game.leaderboard["top_ten"].append(score)
                is_new_score = True

            else:
                index = 0
                for top_ten_score in self.app.game.leaderboard["top_ten"]:
                    if top_ten_score < score:
                        self.app.game.leaderboard["top_ten"][index] = score
                        is_new_score = True
                        break
                    index += 1

            if is_new_score:
                self.app.game.leaderboard["top_ten"].sort()
                self.save_leaderboard()
