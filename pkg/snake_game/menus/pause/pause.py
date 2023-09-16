#!/usr/bin/env python3

"""
    Pause Menu
    ~~~~~~~~~~

    Pause menu shown when the game is paused


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import gc


def pause_menu(self):
    """
    pause_menu
    ~~~~~~~~~~

    pause_menu does stuff
    """

    # Clear previous frame render
    self.game.screen.fill((0, 0, 0, 0))

    # Make sure the right menu option is selected
    self.menu_option = 1
    self.root_menu = 1

    if self.prev_menu is None:
        # Free unreferenced memory
        gc.collect()
        self.prev_menu = 2

    # Pause game music
    self.game.pause_game_music = True

    # Render the paused text
    _ = self.render_button("-Paused-", 10, (255, 0, 0))

    # Get the player score
    score = "NA"
    for obj in self.game.sprite_group.sprites():
        if obj.player:
            score = obj.score

    # Render the score
    _ = self.render_button("Score: " + str(score), 8, (255, 0, 0))

    # Render the quit button
    resume_obj = self.render_button("Resume", 1)

    # Render the settings button
    settings_obj = self.render_button("Settings", -1)

    # Render the quit button
    return_obj = self.render_button("Main Menu", -3)

    menu = [
        (resume_obj, self.game.unpause, 1),
        (settings_obj, self.settings_menu, 1),
        (return_obj, self.home_menu, 1),
    ]

    # Lines used for testing obj limit
    # print(
    #   self.game.sprite_group.sprites()[2].ID,
    #   len(self.game.sprite_group.sprites()[2].children),
    # )

    return menu
