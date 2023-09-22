#!/usr/bin/env python3

"""
    Game Constants


    All constants for the game file

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from pygame.constants import (
    K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT,
)


GAME_TITLE = "Snake"

# Font
REGULAR_FONT = "assets/fonts/PressStart2P-Regular.ttf"
REGULAR_FONT_SIZE = 32

# Music
MUSIC_INTRO = "assets/music/8bit_Stage1_Intro.wav"
MUSIC_LOOP = "assets/music/8bit_Stage1_Loop.wav"

# Sounds
SOUND_SNAKE_DEATH = "assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav"
SOUND_FOOD_PICKUP = "assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav"
SOUND_PORTAL_ENTER = "assets/sounds/8bitsfxpack_windows/SciFi05.wav"

# Sprite sheets
SPRITE_SHEET_SNAKE_PLAYER = "assets/sprites/snake/snake-sheet.png"
SPRITE_SHEET_SNAKE_ENEMY = "assets/sprites/snake/snake_enemy-sheet.png"
SPRITE_SHEET_FOOD = "assets/sprites/food/food-sheet.png"
SPIRTE_SHEET_TELEPORTAL = "assets/sprites/tele_portal/tele_portal-sheet.png"

# Menu options
MENU_HOME = 0
MENU_PAUSE = 1
MENU_SETTINGS = 2
MENU_GAME_OVER = 3
MENU_DISPLAY = 4
MENU_SOUND = 5

# Colors
COLOR_BLACK = (0, 0, 0, 0)
COLOR_RED = (255, 0 , 0)
COLOR_WHITE = (255, 255, 255)
COLOR_PURPLE = (128, 0, 128)
COLOR_GREY = (128,128,128)
COLOR_GREY_DARK = (50,50,50)

# Event input key map
INPUT_KEY_MAP = {
    "W": K_w,
    "A": K_a,
    "S": K_s,
    "D": K_d,
    "Up": K_UP,
    "Down": K_DOWN,
    "Left": K_LEFT,
    "Right": K_RIGHT,
}