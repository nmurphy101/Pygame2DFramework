#!/usr/bin/env python3

"""
    Snake Game


    Defines the game of snake
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import os
import json
import gc
import threading
from datetime import datetime
from typing import Deque

import pygame
from pygame import (
    freetype,
    Surface,
)

from .ai.ai import DecisionBox
from .constants import game_constants as constants
from .entities import (
    Entity,
    Food,
    Snake,
    TelePortal,
)
from .graphics.sprite_sheet import SpriteSheet
from .menus.menus import Menu

from ..app import App


class SnakeGame():
    """SnakeGame

    SnakeGame for the snake
    """


    def __init__(self, alpha_screen: Surface, screen: Surface, app: App):
        """SnakeGame initilizer

        Args:
            alpha_screen (Surface): [description]
            screen (Surface): [description]
            app (App): The gameplatform
        """

        # Calling game platform
        self.app = app

        # Game config file
        self.game_config_file_path = os.path.join(os.path.dirname(__file__), 'game_config.json')
        with open(self.game_config_file_path, encoding="utf8") as json_data_file:
            self.game_config = json.load(json_data_file)

        # Set starting fps from the config file
        self.app.fps = int(self.app.app_config["settings"]["display"]["fps"])

        # Window settings
        self.title = app.title + constants.GAME_TITLE
        pygame.display.set_caption(self.title)
        self.screen = screen
        self.alpha_screen = alpha_screen
        screen_w, screen_h = screen.get_size()
        self.screen_size = (screen_w, screen_h)
        self.game_font = freetype.Font(
            file=constants.REGULAR_FONT,
            size=constants.REGULAR_FONT_SIZE,
        )

        # Game settings
        self.pause_game_music = False
        self.timer = None

        # Game music
        self.game_music_intro = constants.MUSIC_INTRO
        self.game_music_loop = constants.MUSIC_LOOP
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        pygame.mixer.music.load(self.game_music_intro)
        pygame.mixer.music.set_volume(float(self.app.app_config["settings"]["sound"]["music_volume"]))

        # Game Sounds
        self.sounds = [
            pygame.mixer.Sound(constants.SOUND_SNAKE_DEATH),
            pygame.mixer.Sound(constants.SOUND_FOOD_PICKUP),
            pygame.mixer.Sound(constants.SOUND_PORTAL_ENTER),
        ]

        # Game object containers
        self.sprite_group = pygame.sprite.RenderUpdates()
        self.entity_final_scores = {}

        ## Game sprite Sheets
        # Snake Sprite Images
        self.snake_sprite_sheet = SpriteSheet(constants.SPRITE_SHEET_SNAKE_PLAYER)
        self.snake_images = self.snake_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Snake Enemy Sprite Images
        self.snake_enemy_sprite_sheet = SpriteSheet(constants.SPRITE_SHEET_SNAKE_ENEMY)
        self.snake_enemy_images = self.snake_enemy_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Food Sprite images
        self.food_sprite_sheet = SpriteSheet(constants.SPRITE_SHEET_FOOD)
        self.food_images = self.food_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # Teleportal Sprite images
        self.tele_portal_sprite_sheet = SpriteSheet(constants.SPIRTE_SHEET_TELEPORTAL)
        self.tele_portal_images = self.tele_portal_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)


    def play(self, fps_counter_display: callable):
        """play

        play does stuff
        """

        is_fps_display_shown = self.app.app_config["settings"]["display"]["fps_display"]

        # Check if not in a menu
        if self.menu.menu_option is None:

            # clear screen if was in a menu previously
            if self.menu.prev_menu in [0, 1]:
                # Clear previous frame render (from menu)
                self.screen.fill((0, 0, 0, 0))

            # Execute game object actions via parallel threads
            thread_group = []
            for obj in self.sprite_group:
                if not obj.is_alive:
                    continue

                if self.menu.prev_menu in [0, 1]:
                    obj.refresh_draw()

                thread = threading.Thread(target=self._object_actions, args=(obj,))
                thread.start()
                thread_group.append(thread)

            # Wait for threads to finish
            for thread in thread_group:
                thread.join()

            # input("click to continue")

            # Only 1 tick to refresh from pause_menu
            if self.menu.prev_menu in [0, 1]:
                self.menu.prev_menu = None

            # The game loop FPS counter
            if is_fps_display_shown:
                fps_counter_display()

            # Return to app
            return None

        # In a menu
        # The game loop FPS counter
        if is_fps_display_shown:
            fps_counter_display()

        # Show which ever menu option that has been chosen:
        #   Main, Pause, Settings, GameOver, Display, Sound
        return self.menu.menu_options.get(self.menu.menu_option)()


    def _object_actions(self, obj: Entity):
        """_object_actions

        _object_actions does stuff
        """

        # take obj tick actions
        is_updated, is_child_updated = obj.update()

        # Draw game objects
        obj.draw((is_updated, is_child_updated))

        # collision of obj to other objects/children-of-other-objs
        obj.collision_checks(is_updated)


    def start(self):
        """start

        start does stuff
        """
        # Start on a clean slate
        self.clean_up()

        # Check settings
        self.settings_checks()

        # Starting variables
        self.menu.menu_option = None
        self.pause_game_music = False

        # AI blackbox
        self.chosen_ai = DecisionBox(self.app)

        # Initilize game objects - Order of these objects actually matter
        # Food objects
        number_of_food = self.game_config["settings"]["gameplay"]["number_of_food"]

        # if number_of_food <= 0:
        #     raise OSError("1 or more food is required to play")

        for _ in range(number_of_food):
            self.sprite_group.add(Food(self.alpha_screen, self.screen, self.screen_size, self.app))

        # teleporter objects
        teleporter_mod = self.game_config["settings"]["gameplay"]["teleporter_active"]
        if teleporter_mod:
            self.sprite_group.add(TelePortal(self.alpha_screen, self.screen, self.screen_size, self.app))

        # initilize player character
        is_human_playing = self.game_config["settings"]["gameplay"]["human_player"]
        if is_human_playing:
            player_snake = Snake(
                self.alpha_screen, self.screen, self.screen_size, self.app, player=True
            )
            player_snake.speed_mod = self.game_config["settings"]["gameplay"]["player_speed"]
            player_snake.killable = not self.game_config["settings"]["gameplay"]["invinsible_player"]
            self.sprite_group.add(player_snake)

        # initilize ai characters
        number_of_ai = self.game_config["settings"]["gameplay"]["number_of_ai"]
        for _ in range(number_of_ai):
            enemy_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
            enemy_snake.speed_mod = self.game_config["settings"]["gameplay"]["ai_speed"]
            enemy_snake.killable = not self.game_config["settings"]["gameplay"]["invinsible_ai"]
            self.sprite_group.add(enemy_snake)

        # Start the game timer
        self.timer = datetime.now()


    def clean_up(self):
        """clean_up

        clean_up does stuff
        """

        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Game settings
        self.pause_game_music = False

        # Game timer
        self.timer = None

        # Game object list
        for obj in self.sprite_group:
            obj.kill()
        self.sprite_group.empty()

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)

        # Free unreferenced memory
        gc.collect()


    def settings_checks(self):
        """settings_checks

        settings_checks does stuff
        """
        # Start/Restart the game music
        if self.app.app_config["settings"]["sound"]["music"]:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.set_volume(
                float(self.app.app_config["settings"]["sound"]["music_volume"])
            )
            pygame.mixer.music.play(0, 0, 1)

        else:
            pygame.mixer.music.pause()


    def quit_game(self):
        """quit_game

        quit_game does stuff
        """
        self.app.running = False


    def unpause(self):
        """unpause


        unpause does stuff
        """
        self.menu.prev_menu = self.menu.menu_option
        self.menu.menu_option = None
        self.pause_game_music = True



def psudo_func(test):
    """psudo_func

    psudo_func does stuff
    """
    print("Psudo_func: ", test)
