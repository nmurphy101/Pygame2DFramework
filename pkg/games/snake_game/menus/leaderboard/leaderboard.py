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

    # Clear previous frame render
    self.app.game.screen.fill(COLOR_BLACK)

    # Make sure the right menu option is selected
    self.menu_option = MENU_LEADERBOARD

    # Render the Leaderboard text
    _ = self.render_button("Leaderboard", 10, color=COLOR_RED)

    # initilize menu
    menu = []

    # Render the Return button
    back_obj = self.render_button("Back", -9)
    menu.append((back_obj, self.menu_options[MENU_HOME], self.prev_menu))

    # Render the highscore
    highscore = self.app.game.leaderboard["highscore"]
    highscore_obj = self.render_button(f"HIGH-SCORE: {highscore}", 8)
    menu.append((highscore_obj, None, self.prev_menu))

    # Render the top 10 scores
    self.app.game.leaderboard["top_ten"].sort(reverse=True)

    index = 7
    ranking = 1
    for score in self.app.game.leaderboard["top_ten"]:
        _ = self.render_button(f"{ranking}:", index, w_offset=20, h_offset=-50)
        _ = self.render_button(score, index, w_offset=20, h_offset=50)
        index -= 1.5
        ranking += 1

    return menu