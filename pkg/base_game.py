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

    def __init__(self, alpha_screen: Surface, screen: Surface, app: App):
        """SnakeGame initilizer

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

        # Game screens
        self.screen = screen
        self.alpha_screen = alpha_screen
        game_width = self.app.screen_width - (self.app.screen_width % self.grid_size)
        game_height = self.app.screen_height - (self.app.screen_height % self.grid_size)
        self.screen_size = (game_width, game_height)

        # Game object containers
        self.sprite_group = sprite.RenderUpdates()

