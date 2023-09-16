#!/usr/bin/env python3

"""
    Snake Game
    ~~~~~~~~~~

    Defines the game of snake

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


import gc
from datetime import datetime
from typing import Deque

import pygame
from pygame import (
    freetype,
    Surface,
)

# All the game entities
from .entities import (
    Snake, Food, TelePortal,
)

# All the game menus
from .menus.menus import Menu
from .ai.ai import DecisionBox
from .graphics.sprite_sheet import SpriteSheet

# The main app
from ..app import App


class SnakeGame():
    """
    SnakeGame
    ~~~~~~~~~~

    SnakeGame for the snake
    """


    def __init__(self, alpha_screen: Surface, screen: Surface, app: App):
        """
        SnakeGame initilizer

        Args:
            alpha_screen (Surface): The screen the game plays on
            screen (Surface): [description]
            app (App): The gameplatform
        """

        # Calling game platform
        self.app = app

        # Set starting fps from the config file
        self.app.fps = int(self.app.game_config["settings"]["display"]["fps"])

        # Window settings
        self.title = app.title + "Snake"
        pygame.display.set_caption(self.title)
        self.screen = screen
        self.alpha_screen = alpha_screen
        screen_w, screen_h = screen.get_size()
        self.screen_size = (screen_w, screen_h)
        self.game_font = freetype.Font(
            file='assets/fonts/PressStart2P-Regular.ttf',
            size=32,
        )

        # Game settings
        self.pause_game_music = False
        self.timer = None

        # Game music
        self.game_music_intro = "assets/music/8bit_Stage1_Intro.wav"
        self.game_music_loop = "assets/music/8bit_Stage1_Loop.wav"
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        pygame.mixer.music.load(self.game_music_intro)
        pygame.mixer.music.set_volume(float(self.app.game_config["settings"]["sound"]["music_volume"]))

        # Game Sounds
        self.sounds = [
            pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/MISC-NOISE-BIT_CRUSH/Retro_8-Bit_Game-Misc_Noise_06.wav"),
            pygame.mixer.Sound("assets/sounds/8bitretro_soundpack/PICKUP-COIN-OPJECT-ITEM/Retro_8-Bit_Game-Pickup_Object_Item_Coin_01.wav"),
            pygame.mixer.Sound("assets/sounds/8bitsfxpack_windows/SciFi05.wav"),
        ]

        # Game object containers
        self.sprite_group = pygame.sprite.RenderUpdates()
        self.dirty_rects = Deque()

        ## Game sprite Sheets
        # Snake Sprite Images
        self.snake_sprite_sheet = SpriteSheet("assets/sprites/snake/snake-sheet.png")
        self.snake_images = self.snake_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Snake Enemy Sprite Images
        self.snake_enemy_sprite_sheet = SpriteSheet("assets/sprites/snake/snake_enemy-sheet.png")
        self.snake_enemy_images = self.snake_enemy_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Food Sprite images
        self.food_sprite_sheet = SpriteSheet("assets/sprites/food/food-sheet.png")
        self.food_images = self.food_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # Teleportal Sprite images
        self.tele_portal_sprite_sheet = SpriteSheet("assets/sprites/tele_portal/tele_portal-sheet.png")
        self.tele_portal_images = self.tele_portal_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)


    def play(self, update_fps):
        """
        play
        ~~~~~~~~~~

        play does stuff
        """

        is_fps_display_shown = self.app.game_config["settings"]["display"]["fps_display"]

        # Check if not in a menu
        if self.menu.menu_option is None:

            fill_screen = self.screen.fill

            # Execute game object actions
            for obj in self.sprite_group:
                # Make sure to refresh coming out of pause_menu
                if self.menu.prev_menu in [0, 1]:
                    # Clear previous frame render (from menu)
                    fill_screen((0, 0, 0, 0))

                    # Draw game objects
                    obj.draw(self.sprite_group, (True, True))

                # take obj tick actions
                updated = obj.update(self.sprite_group)

                # Draw game objects
                obj.draw(self.sprite_group, (updated, False))

                # collision of obj to other objects/children-of-other-objs
                obj.collision_checks(updated)

            # Only 1 tick to refresh from pause_menu
            if self.menu.prev_menu in [0, 1]:
                self.menu.prev_menu = None

            # The game loop FPS counter
            if is_fps_display_shown:
                self.dirty_rects.append(update_fps())
                update_fps()

            # Return to app
            return None, self.dirty_rects

        # In a menu
        # The game loop FPS counter
        if is_fps_display_shown:
            update_fps()

        # Show which ever menu option that has been chosen:
        #   Main, Pause, Settings, GameOver, Display, Sound
        return self.menu.menu_options.get(self.menu.menu_option)(), None


    def start(self):
        """
        start
        ~~~~~~~~~~

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
        self.chosen_ai = DecisionBox()

        # Initilize game objects - Order of these objects actually matter
        # Food objects
        number_of_food = self.app.game_config["settings"]["gameplay"]["number_of_food"]
        for _ in range(number_of_food):
            self.sprite_group.add(Food(self.alpha_screen, self.screen, self.screen_size, self.app))

        # teleporter objects
        teleporter_mod = self.app.game_config["settings"]["gameplay"]["teleporter_active"]
        if teleporter_mod:
            self.sprite_group.add(TelePortal(self.alpha_screen, self.screen, self.screen_size, self.app))

        # initilize player character
        is_human_playing = self.app.game_config["settings"]["gameplay"]["human_player"]
        if is_human_playing:
            player_snake = Snake(
                self.alpha_screen, self.screen, self.screen_size, self.app, player=True
            )
            player_snake.speed_mod = self.app.game_config["settings"]["gameplay"]["player_speed"]
            player_snake.killable = not self.app.game_config["settings"]["gameplay"]["invinsible_player"]
            self.sprite_group.add(player_snake)

        # initilize ai characters
        number_of_ai = self.app.game_config["settings"]["gameplay"]["number_of_ai"]
        for _ in range(number_of_ai):
            enemy_snake = Snake(self.alpha_screen, self.screen, self.screen_size, self.app)
            enemy_snake.speed_mod = self.app.game_config["settings"]["gameplay"]["ai_speed"]
            enemy_snake.killable = not self.app.game_config["settings"]["gameplay"]["invinsible_ai"]
            self.sprite_group.add(enemy_snake)

        # Start the game timer
        self.timer = datetime.now()


    def clean_up(self):
        """
        clean_up
        ~~~~~~~~~~

        clean_up does stuff
        """

        # Clear previous frame render
        self.screen.fill((0, 0, 0, 0))

        # Game settings
        self.pause_game_music = False

        # Game timer
        self.timer = None

        # Game object list
        self.sprite_group.empty()

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)

        # Free unreferenced memory
        gc.collect()


    def settings_checks(self):
        """
        settings_checks
        ~~~~~~~~~~

        settings_checks does stuff
        """
        # Start the game music
        if self.app.game_config["settings"]["sound"]["music"]:
            self.current_track = 0
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.set_volume(
                float(self.app.game_config["settings"]["sound"]["music_volume"])
            )
            pygame.mixer.music.play(0, 0, 1)

        else:
            pygame.mixer.music.pause()


    def quit_game(self):
        """
        quit_game
        ~~~~~~~~~~

        quit_game does stuff
        """
        self.app.running = False


    def unpause(self):
        """
        unpause
        ~~~~~~~~~~

        unpause does stuff
        """
        self.menu.prev_menu = self.menu.menu_option
        self.menu.menu_option = None
        self.pause_game_music = True


def psudo_func(test):
    """
    psudo_func
    ~~~~~~~~~~

    psudo_func does stuff
    """
    print("Psudo_func: ", test)
