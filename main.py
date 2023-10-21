#!/usr/bin/env python3

"""
    Snake Game - Main

    It's snake.

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv2, see LICENSE for more details.
"""


__author__ = "Nicholas Murphy"
__version__ = '1.0.3-alpha'


from functools import wraps
from io import StringIO
from sys import exit as sys_exit

from cProfile import Profile
from pstats import Stats
from pygame import (
    display as pygame_display,
    quit as pygame_quit,
    image as pygame_image,
)

from pkg.app import App
from pkg.games.snake_game import Game as SnakeGame


# profiling decorator
def profiling():
    """Profiler

    decorator for game processing optimization
    """

    def _profiling(function_param):
        @wraps(function_param)
        def __profiling(*rgs, **kwargs):
            profile = Profile()
            profile.enable()

            result = function_param(*rgs, **kwargs)

            profile.disable()

            # save readable stats into file
            string_io = StringIO()
            profile_stats = Stats(profile, stream=string_io).sort_stats("tottime")

            # skip strip_dirs() if you want to see full path's
            profile_stats.print_stats()

            with open("logs/profile.txt", "w+", encoding="utf8") as output_file:
                output_file.write(string_io.getvalue())

            return result

        return __profiling

    return _profiling


@profiling()
def main():
    """main

    The main app startup
    """

    # Import and set the window icon
    icon = pygame_image.load("_internal/assets/icons/favicon.ico")
    pygame_display.set_icon(icon)

    # Import all the game objects from the package names
    game_module_list = [SnakeGame]

    # Initilize the base game with the game options
    app = App(game_module_list)

    # Run the loaded game from the app platform
    app.run()

    # Quit the game
    pygame_display.quit()

    pygame_quit()

    sys_exit()


if __name__ == "__main__":
    main()
