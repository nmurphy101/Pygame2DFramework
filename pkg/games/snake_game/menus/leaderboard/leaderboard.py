#!/usr/bin/env python3

"""
    Home Menu

    Game Home menu

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from .....menus import Menu

from ...constants.game_constants import (
    COLOR_BLACK,
    COLOR_RED,
    MENU_LEADERBOARD,
    MENU_HOME,
)


def leaderboard_menu(self: Menu):
    """leaderboard_menu

    leaderboard_menu does stuff
    """

    if self.refresh or self.menu_option != MENU_LEADERBOARD:
        # Clear previous frame render
        self.app.game.screen.fill(COLOR_BLACK)

        # Make sure the right menu option is selected
        self.menu_option = MENU_LEADERBOARD

        # Render the Leaderboard text
        self.render_text("Leaderboard", 10, color=COLOR_RED)

        # Render the Return button
        back_obj = self.render_button("Back", -9, has_outline=True)

        # Render the highscore
        highscore = self.app.game.leaderboard["highscore"]
        _ = self.render_text(f"HIGH-SCORE: {highscore}", 8)

        # Render the top 10 scores
        self.app.game.leaderboard["top_ten"].sort(reverse=True)

        index = 7
        ranking = 1
        for score in self.app.game.leaderboard["top_ten"]:
            self.render_text(f"{ranking}:", index, w_offset=20, h_offset=-50)
            self.render_text(score, index, w_offset=20, h_offset=50)
            index -= 1.5
            ranking += 1

        self.menu = [
            (back_obj, self.menu_options[MENU_HOME], MENU_LEADERBOARD, None)
        ]

        self.refresh = False

    return self.menu
