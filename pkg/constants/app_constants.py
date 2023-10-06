#!/usr/bin/env python3

"""
    App Constants


    All constants for the app

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


# filenames
CONFIG_FILE_NAME = "app_config.json"
LOG_FILE_NAME = "output.log"

# Font
REGULAR_FONT = "assets/fonts/PressStart2P-Regular.ttf"
REGULAR_FONT_SIZE = 32

# ui sounds
SOUND_UI_HOVER = "assets/sounds/8bitsfxpack_windows/UI01.wav"
SOUND_UI_FORWARD = "assets/sounds/8bitsfxpack_windows/UI02.wav"
SOUND_UI_BACKWARD = "assets/sounds/8bitsfxpack_windows/UI03.wav"

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0 , 0)
COLOR_WHITE = (255, 255, 255)
COLOR_PURPLE = (128, 0, 128)
COLOR_GREY = (128,128,128)
COLOR_GREY_DARK = (50,50,50)

# Dimensions
X = 0
Y = 1
WIDTH = 0
HEIGHT = 1

# Menu options
MENU_HOME = 0
MENU_PAUSE = 1
MENU_SETTINGS = 2
MENU_GAME_OVER = 3
MENU_DISPLAY = 4
MENU_SOUND = 5
MENU_KEYBINDING = 6
MENU_GAMEPLAY = 7
MENU_LEADERBOARD = 8

# Mouse down event map
MOUSE_DOWN_MAP = {
    1: "left",
    2: "middle",
    3: "right",
    4: "scroll_up",
    5: "scroll_down",
}