#!/usr/bin/env python3

"""
    Base game obj


    The base of all game classes
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from typing import TypedDict

from pygame import (
    display,
    draw,
    freetype,
    mixer,
    sprite,
    Surface,
    transform,
)

from .app import App


class BaseGame():
    """Game

    The main object for any game to be created
    Required to be the called parent obj of any created game
    """

    def __init__(self, app: App, alpha_screen: Surface, screen: Surface):
        """BaseGame initilizer

        Args:
            alpha_screen (Surface): [description]
            screen (Surface): [description]
            app (App): The gameplatform
        """

        # Calling game platform
        self.app = app

        # Window settings
        self.title = app.title + self.TITLE
        display.set_caption(self.title)

        # Game board grid size (also sprite size modifer)
        self.grid_size = self.game_config["settings"]["gameplay"]["grid_size"]

        # Game bar
        self.game_bar_height = self.grid_size * 3

        # Game screens
        self.screen = screen
        self.alpha_screen = alpha_screen
        game_width = self.app.screen_width - (self.app.screen_width % self.grid_size) - self.grid_size
        game_height = self.app.screen_height - (self.app.screen_height % self.grid_size) - self.grid_size
        game_top = self.game_bar_height
        game_left = 0
        self.screen_size = (game_width, game_height, game_top, game_left)

        # Game object containers
        self.sprite_group = sprite.RenderUpdates()

