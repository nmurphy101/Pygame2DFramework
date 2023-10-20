#!/usr/bin/env python3

"""
    App Constants


    All constants for the app

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


# filenames
CONFIG_APP_FILE_NAME = "app_config.json"
LOG_FILE_NAME = "output.log"

# Font
REGULAR_FONT = "_internal/assets/fonts/PressStart2P-Regular.ttf"
REGULAR_FONT_SIZE = 32

# ui sounds
SOUND_UI_HOVER = "_internal/assets/sounds/8bitsfxpack_windows/UI01.wav"
SOUND_UI_FORWARD = "_internal/assets/sounds/8bitsfxpack_windows/UI02.wav"
SOUND_UI_BACKWARD = "_internal/assets/sounds/8bitsfxpack_windows/UI03.wav"

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

# Default app config
DEFAULT_APP_CONFIG = {
    "settings": {
        "sound": {
            "music": true,
            "music_volume": 0.05,
            "effect_volume": 0.1,
            "menu_volume": "0.1"
        },
        "display": {
            "fps": 3000,
            "fps_display": false,
            "fullscreen": false,
            "resolution": "1280x720",
            "window_title": "Game Platform - "
        },
        "debug": {
            "log_level": "debug",
            "debug_mode": false
        }
    }
}