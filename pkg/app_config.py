#!/usr/bin/env python3

"""
    App config obj


    The structure of the app config file
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""

from typing import TypedDict


class SoundConfig(TypedDict):
    music: bool
    music_volume: str
    effect_volume: str
    menu_volume: str


class DisplayConfig(TypedDict):
    fps: int
    fps_display: bool
    fullscreen: bool
    resolution: str
    window_title: str


class DebugConfig(TypedDict):
    log_level: str


class SettingsConfig(TypedDict):
    sound: SoundConfig
    display: DisplayConfig
    debug: DebugConfig


class AppConfig(TypedDict):
    settings: SettingsConfig
