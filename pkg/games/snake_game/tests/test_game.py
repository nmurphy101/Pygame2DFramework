#!/usr/bin/env python3

"""
    Test Game

    Defines all the tests for the game.py file
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import pytest
from unittest.mock import MagicMock

from pkg.games.snake_game.game import is_multiple_of_4
# from pkg.games.snake_game.game import SnakeGame
# from pkg.app import App

# app = App([SnakeGame])
# app.game = SnakeGame(app, app.alpha_screen, app.screen)

class TestGameMethods:
    def test_is_multiple_of_4(self):

        is_multiple_of_4_mock = MagicMock(wraps=is_multiple_of_4)

        assert is_multiple_of_4_mock(5) == False
        assert  is_multiple_of_4_mock(4) == True

    # def test_start(self):
    #     app.game.start()
    #     assert True