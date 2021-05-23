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
import io
import pstats
import cProfile
from functools import wraps
from pkg.snake_game.game import SnakeGame
from pkg.app import App

# freeze_support()
# profiling decorator
def profiling():
    def _profiling(f):
        @wraps(f)
        def __profiling(*rgs, **kwargs):
            pr = cProfile.Profile()
            pr.enable()

            result = f(*rgs, **kwargs)

            pr.disable()
            # save readable stats into file
            s = io.StringIO()
            p = pstats.Stats(pr, stream=s).sort_stats("tottime")
            # skip strip_dirs() if you want to see full path's
            p.print_stats()
            with open('profile.txt', 'w+') as output_file:
                output_file.write(s.getvalue())
            return result
        return __profiling
    return _profiling

@profiling()
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
    #pylint: disable=no-member
    #pylint: disable=no-member
    # pygame.display.quit()
    # pygame.quit()
    #pylint: enable=no-member
    # sys.exit()
    #pylint: enable=no-member


if __name__ == "__main__":
    main()
