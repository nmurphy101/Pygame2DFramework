#!/usr/bin/env python3

"""
    Snake Game - Main
    ~~~~~~~~~~

    It's snake.

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv2, see LICENSE for more details.
"""


__author__ = "Nicholas Murphy"
__version__ = '1.0.0-alpha'

# from tkinter import Tk
# from multiprocessing import Manager
# from multiprocessing import freeze_support
from pkg.snake_game.game import SnakeGame
from pkg.app import App

# freeze_support()

def main():
    '''
    main
    '''
    # Take the game to be initalized
    snake_game = SnakeGame
    # Initilize the base game with the imported game
    game = App(snake_game)
    # Run the loaded game
    game.run()


if __name__ == "__main__":
    main()
