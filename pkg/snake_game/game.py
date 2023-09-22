#!/usr/bin/env python3

"""
    Snake Game


    Defines the game of snake
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from os import path
from json import load
from gc import collect as gc_collect
from threading import Thread
from datetime import datetime
from typing import Deque

from pygame import (
    display,
    draw,
    freetype,
    mixer,
    sprite,
    Surface,
)

from .ai.ai import DecisionBox
from .constants import (
    COLOR_BLACK,
    COLOR_GREY,
    COLOR_GREY_DARK,
    COLOR_RED,
    COLOR_PURPLE,
    GAME_TITLE,
    REGULAR_FONT,
    REGULAR_FONT_SIZE,
    MUSIC_INTRO,
    MUSIC_LOOP,
    SOUND_SNAKE_DEATH,
    SOUND_FOOD_PICKUP,
    SOUND_PORTAL_ENTER,
    SPRITE_SHEET_SNAKE_PLAYER,
    SPRITE_SHEET_SNAKE_ENEMY,
    SPRITE_SHEET_FOOD,
    SPIRTE_SHEET_TELEPORTAL,
)
from .entities import (
    Entity,
    Food,
    Snake,
    TelePortal,
)
from .graphics.sprite_sheet import SpriteSheet
from .menus.menus import Menu

from ..app import App


def is_multiple_of_4(number):
    """
    Verify if a number is a multiple of 4.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is a multiple of 4, False otherwise.
    """
    return number % 4 == 0


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
        self.game_config_file_path = path.join(path.dirname(__file__), 'game_config.json')
        with open(self.game_config_file_path, encoding="utf8") as json_data_file:
            self.game_config = load(json_data_file)

        # Set starting fps from the config file
        self.app.fps = int(self.app.app_config["settings"]["display"]["fps"])

        # Game settings
        self.pause_game_music = False
        self.timer = None
        self.grid_size = self.game_config["settings"]["gameplay"]["grid_size"]

        # Window settings
        self.title = app.title + GAME_TITLE
        display.set_caption(self.title)
        self.screen = screen
        self.alpha_screen = alpha_screen
        screen_w, screen_h = screen.get_size()
        self.game_bar_height = self.grid_size * 3
        self.screen_size = (screen_w, screen_h + self.game_bar_height)

        # Game fonts
        self.game_font = freetype.Font(
            file=REGULAR_FONT,
            size=REGULAR_FONT_SIZE,
        )

        if not is_multiple_of_4(self.grid_size):
            raise OSError("grid_size must be a multiple of 4")

        # Game music
        self.game_music_intro = MUSIC_INTRO
        self.game_music_loop = MUSIC_LOOP
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        mixer.music.load(self.game_music_intro)
        mixer.music.set_volume(float(self.app.app_config["settings"]["sound"]["music_volume"]))

        # Game Sounds
        self.sounds = [
            mixer.Sound(SOUND_SNAKE_DEATH),
            mixer.Sound(SOUND_FOOD_PICKUP),
            mixer.Sound(SOUND_PORTAL_ENTER),
        ]

        # Game object containers
        self.sprite_group = sprite.RenderUpdates()
        self.entity_final_scores = {}

        ## Game sprite Sheets
        # Snake Sprite Images
        self.snake_sprite_sheet = SpriteSheet(SPRITE_SHEET_SNAKE_PLAYER)
        self.snake_images = self.snake_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Snake Enemy Sprite Images
        self.snake_enemy_sprite_sheet = SpriteSheet(SPRITE_SHEET_SNAKE_ENEMY)
        self.snake_enemy_images = self.snake_enemy_sprite_sheet.load_grid_images(
            (2, 8),
            (1, 1),
            (1, 1),
        )

        # Food Sprite images
        self.food_sprite_sheet = SpriteSheet(SPRITE_SHEET_FOOD)
        self.food_images = self.food_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # Teleportal Sprite images
        self.tele_portal_sprite_sheet = SpriteSheet(SPIRTE_SHEET_TELEPORTAL)
        self.tele_portal_images = self.tele_portal_sprite_sheet.load_grid_images(
            (1, 1),
            (1, 1),
            (1, 1),
        )

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)


    def play(self):
        """play

        play does stuff
        """

        # Check if not in a menu
        if self.menu.menu_option is None:

            # clear screen if was in a menu previously
            if self.menu.prev_menu in [0, 1]:
                # Clear previous frame render (from menu)
                self.app.game.screen.fill(COLOR_BLACK)

            # Execute game object actions via parallel threads
            thread_group = []
            for obj in self.sprite_group:
                if not obj.is_alive:
                    continue

                if self.menu.prev_menu in [0, 1]:
                    obj.refresh_draw()

                thread = Thread(target=self._object_actions, args=(obj,))
                thread.start()
                thread_group.append(thread)

            # Wait for threads to finish
            for thread in thread_group:
                thread.join()

            # input("click to continue")

            # Only 1 tick to refresh from pause_menu
            if self.menu.prev_menu in [0, 1]:
                self.menu.prev_menu = None

            # show the game bar at top of screen
            self.game_bar_display()

            # Return to app
            return None

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
            self.sprite_group.add(Food(self.screen_size, self.app))

        # teleporter objects
        teleporter_mod = self.game_config["settings"]["gameplay"]["teleporter_active"]
        if teleporter_mod:
            self.sprite_group.add(TelePortal(self.screen_size, self.app))

        # initilize player character
        is_human_playing = self.game_config["settings"]["gameplay"]["human_player"]
        if is_human_playing:
            player_snake = Snake(
                self.screen_size, self.app, player=True
            )
            player_snake.speed_mod = self.game_config["settings"]["gameplay"]["player_speed"]
            player_snake.killable = not self.game_config["settings"]["gameplay"]["invinsible_player"]
            self.sprite_group.add(player_snake)

        # initilize ai characters
        number_of_ai = self.game_config["settings"]["gameplay"]["number_of_ai"]
        for _ in range(number_of_ai):
            enemy_snake = Snake(self.screen_size, self.app)
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
        self.app.game.screen.fill(COLOR_BLACK)

        # Game settings
        self.pause_game_music = False

        # Game timer
        self.timer = None

        # Reset the final player score
        self.entity_final_scores = {}

        # Game objects cleanup
        for obj in self.sprite_group:
            obj.sight_lines_diag = None

            obj.sight_lines = None

            for child in obj.children:
                child.kill()

            obj.children = None

            obj.kill()

        self.sprite_group.empty()

        # AI blackbox
        self.chosen_ai = None

        # Menu Obj
        self.menu = Menu(self)

        # Free unreferenced memory
        gc_collect()


    def settings_checks(self):
        """settings_checks

        settings_checks does stuff
        """
        # Start/Restart the game music
        if self.app.app_config["settings"]["sound"]["music"]:
            mixer.music.load(self.playlist[self.current_track])
            mixer.music.set_volume(
                float(self.app.app_config["settings"]["sound"]["music_volume"])
            )
            mixer.music.play(0, 0, 1)

        else:
            mixer.music.pause()


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


    def game_bar_display(self):
        """game_bar_display

        Returns:
            [type]: [description]
        """

        # Clear previous frame obj's location with the game bar color
        game_bar_pos = (0, 0, self.screen_size[0], self.game_bar_height)
        draw.rect(self.screen, COLOR_GREY_DARK, game_bar_pos)

        game_bar_pos = (0, self.game_bar_height-2, self.screen_size[0], 2)
        draw.rect(self.screen, COLOR_GREY, game_bar_pos)

        score = 0
        for _, value in self.entity_final_scores.items():
            if value["is_player"]:
                score = value["score"]

        _ = self.menu.render_button(f"Score:{score}", .35, -1, color=COLOR_RED, clear_background=False, relative_from="top")
