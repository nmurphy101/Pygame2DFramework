#!/usr/bin/env python3

"""
    Game config obj


    The structure of all game config files
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from typing import TypedDict


# Game json config file
class GameplayConfig(TypedDict):
    human_player: bool
    teleporter: bool
    inv_player: bool
    inv_ai: bool
    num_ai: int
    ai_difficulty: int
    ai_speed: int
    player_speed: int
    num_of_food: int
    grid_size: int


class KeybindingsConfig(TypedDict):
    move_up: str
    move_left: str
    move_down: str
    move_right: str


class SettingsConfig(TypedDict):
    gameplay: GameplayConfig
    keybindings: KeybindingsConfig


class GameConfig(TypedDict):
    settings: SettingsConfig


# Leaderboard json config file
class LeaderBoard(TypedDict):
    highscore: int
    top_ten: list[int]