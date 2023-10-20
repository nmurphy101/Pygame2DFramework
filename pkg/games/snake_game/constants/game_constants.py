#!/usr/bin/env python3

"""
    Game Constants


    All constants for the game file

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from pygame.constants import (
    K_q, K_w, K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p,
    K_a, K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l,
    K_z, K_x, K_c, K_v, K_b, K_n, K_m,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
)


GAME_TITLE = "Snake"

# filenames
CONFIG_GAME_FILE_NAME = "game_config.json"

# Font
REGULAR_FONT = "_internal/assets/fonts/PressStart2P-Regular.ttf"
REGULAR_FONT_SIZE = 32

# Music
MUSIC_INTRO = "_internal/assets/music/8bit_Stage1_Intro.wav"
MUSIC_LOOP = "_internal/assets/music/8bit_Stage1_Loop.wav"

# Sounds
SOUND_SNAKE_DEATH = "_internal/assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav"
SOUND_FOOD_PICKUP = "_internal/assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav"
SOUND_PORTAL_ENTER = "_internal/assets/sounds/8bitsfxpack_windows/SciFi05.wav"

# Sprite sheets
SPRITE_SHEET_SNAKE_PLAYER = "_internal/assets/sprites/snake/snake-sheet.png"
SPRITE_SHEET_SNAKE_ENEMY = "_internal/assets/sprites/snake/snake_enemy-sheet.png"
SPRITE_SHEET_FOOD = "_internal/assets/sprites/food/food-sheet.png"
SPIRTE_SHEET_TELEPORTAL = "_internal/assets/sprites/tele_portal/tele_portal-sheet.png"

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
UP_RIGHT = .5
RIGHT_DOWN = 1.5
DOWN_LEFT = 2.5
LEFT_UP = 3.5
DIRECTION_MAP = {
    0: "UP",
    .5: "UP_RIGHT",
    1: "RIGHT",
    1.5: "RIGHT_DOWN",
    2: "DOWN",
    2.5: "DOWN_LEFT",
    3: "LEFT",
    3.5: "LEFT_UP",
}

# Dimensions
X = 0
Y = 1
NAME = 2
WIDTH = 0
HEIGHT = 1
TOP = 2

# Sound indexes
SOUND_SNAKE_DEATH_IDX = 0
SOUND_FOOD_PICKUP_IDX = 1
SOUND_PORTAL_ENTER_IDX = 2

# Logic indexes
POS_IDX = 0
DIST_FROM_SELF_IDX = 1
ENTITY = 0
CHILD = 1

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

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0 , 0)
COLOR_WHITE = (255, 255, 255)
COLOR_PURPLE = (128, 0, 128)
COLOR_GREY = (128,128,128)
COLOR_GREY_DARK = (50,50,50)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# Event input key map
INPUT_KEY_MAP = {
    "Q": K_q,
    "W": K_w,
    "E": K_e,
    "R": K_r,
    "T": K_t,
    "Y": K_y,
    "U": K_u,
    "I": K_i,
    "O": K_o,
    "P": K_p,
    "A": K_a,
    "S": K_s,
    "D": K_d,
    "F": K_f,
    "G": K_g,
    "H": K_h,
    "J": K_j,
    "K": K_k,
    "L": K_l,
    "Z": K_z,
    "X": K_x,
    "C": K_c,
    "V": K_v,
    "B": K_b,
    "N": K_n,
    "M": K_m,
    "Up": K_UP,
    "Down": K_DOWN,
    "Left": K_LEFT,
    "Right": K_RIGHT,
}

# Human readable setting names
DISPLAY_SETTING_MAP = {
    "human_player": "Player",
    "killable_player": "Pla.Killable",
    "player_speed": "Player Speed",
    "num_ai": "Number of AI",
    "killable_ai": "AI Killable",
    "ai_speed": "AI Speed",
    "ai_difficulty": "AI Skill",
    "teleporter": "Teleporter",
    "visible_sight_lines": "Sightlines",
    "num_of_food": "Number Food",
    "grid_size": "Grid Size",
    "move_up": "Up",
    "move_left": "Left",
    "move_down": "Down",
    "move_right": "Right",
    True: "Yes",
    False: "No",
}

INV_DISPLAY_SETTING_MAP = {v: k for k, v in DISPLAY_SETTING_MAP.items()}

# Default game config data
DEFAULT_GAME_CONFIG = {
    "settings": {
        "gameplay": {
            "human_player": False,
            "killable_player": False,
            "player_speed": 0.7,
            "num_ai": 8,
            "killable_ai": True,
            "ai_difficulty": 10,
            "ai_speed": 3.6,
            "teleporter": True,
            "visible_sight_lines": False,
            "num_of_food": 6,
            "grid_size": 16
        },
        "keybindings": {
            "move_up": "W",
            "move_left": "A",
            "move_down": "S",
            "move_right": "D"
        }
    }
}

# Default leaderboard data
DEFAULT_LEADERBOARD = {
    "highscore": 150,
    "top_ten": [
        20,
        20,
        30,
        30,
        30,
        50,
        90,
        130,
        140,
        150
    ]
}