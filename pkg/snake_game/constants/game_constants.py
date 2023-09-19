#!/usr/bin/env python3

"""
    Game Constants
    ~~~~~~~~~~

    All constants for the game file


    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

import math
from datetime import datetime, timedelta

import pygame

GAME_TITLE = "Snake"
REGULAR_FONT = "assets/fonts/PressStart2P-Regular.ttf"

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