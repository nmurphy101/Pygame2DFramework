#!/usr/bin/env python3

"""
    Game


    Defines the game of snake
    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from gc import collect as gc_collect
from json import dump as json_dump, load as json_load
from logging import (
    info as logging_info,
)
import numpy as np
from os import path
from pathlib import Path
from threading import Thread

from pygame import (
    display as pygame_display,
    draw,
    error as pygame_error,
    font as pygame_font,
    freetype as pygame_freetype,
    mixer as pygame_mixer,
    sndarray as pygame_sndarray,
    sprite,
    Surface,
    transform,
)

from .ai import DecisionBox, Node
from .constants import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_GREY,
    COLOR_GREY_DARK,
    COLOR_RED,
    COLOR_WHITE,
    DEFAULT_GAME_CONFIG,
    DEFAULT_LEADERBOARD,
    GAME_TITLE,
    REGULAR_FONT,
    REGULAR_FONT_SIZE,
    MENU_HOME,
    MENU_PAUSE,
    MENU_SETTINGS,
    MENU_GAME_OVER,
    MENU_KEYBINDING,
    MENU_GAMEPLAY,
    MENU_LEADERBOARD,
    MUSIC_INTRO,
    MUSIC_LOOP,
    SOUND_SNAKE_DEATH,
    SOUND_FOOD_PICKUP,
    SOUND_PORTAL_ENTER,
    SPRITE_SHEET_SNAKE_PLAYER,
    SPRITE_SHEET_SNAKE_ENEMY,
    SPRITE_SHEET_FOOD,
    SPIRTE_SHEET_TELEPORTAL,
    X,
    Y,
    WIDTH,
    HEIGHT,
)
from .entities import (
    Entity,
    Food,
    Snake,
    TelePortal,
)
from .graphics.sprite_sheet import SpriteSheet
from .menus import (
    home_menu,
    pause_menu,
    settings_menu,
    game_over_menu,
    keybinding_menu,
    gameplay_menu,
    leaderboard_menu,
)

from .game_configs import GameConfig, LeaderBoard

from pkg.app import App
from pkg.base_game import BaseGame


class SnakeGame(BaseGame):
    """SnakeGame

    The main object for playing the game of snake.
    """

    TITLE = GAME_TITLE


    def __init__(self, app: App, alpha_screen: Surface, screen: Surface):
        """SnakeGame initilizer

        Args:
            alpha_screen (Surface): [description]
            screen (Surface): [description]
            app (App): The gameplatform
        """

        logging_info("Initilizing snake game obj")
        self.screen = screen
        self.alpha_screen = alpha_screen

        # Show loading screen
        app._display_loading_screen(self.screen)

        logging_info("Loading Game config: Working")
        # Game config file
        self.game_config_file_path = path.join(path.dirname(__file__), "game_config.json")

        try:
            with open(self.game_config_file_path, encoding="utf8") as json_data_file:
                self.game_config: GameConfig = json_load(json_data_file)

        except FileNotFoundError:
            self.game_config = DEFAULT_GAME_CONFIG
            Path(path.dirname(__file__)).mkdir(parents=True, exist_ok=True)
            with open(self.game_config_file_path, "w+", encoding="utf8") as _file:
                json_dump(self.game_config, _file, ensure_ascii=False, indent=4)

        logging_info("Loading Gameconfig: Finished")

        logging_info("Loading Game leaderboard: Working")
        # Game leaderboard file
        self.leaderboard_file_path = path.join(path.dirname(__file__), "leaderboard.json")

        try:
            with open(self.leaderboard_file_path, encoding="utf8") as json_data_file:
                self.leaderboard: LeaderBoard = json_load(json_data_file)

        except FileNotFoundError:
            self.leaderboard = DEFAULT_LEADERBOARD
            Path(path.dirname(__file__)).mkdir(parents=True, exist_ok=True)
            with open(self.leaderboard_file_path, "w+", encoding="utf8") as _file:
                json_dump(self.leaderboard, _file, ensure_ascii=False, indent=4)

        logging_info("Loading Game leaderboard: Finished")

        # Initilize parent init
        super().__init__(app, alpha_screen, screen)

        if not is_multiple_of_4(self.grid_size):
            raise OSError("grid_size must be a multiple of 4")

        # Game fonts
        try:
            self.game_font = pygame_freetype.Font(
                file=REGULAR_FONT,
                size=REGULAR_FONT_SIZE,
            )
        except:
            self.app_font = pygame_freetype.SysFont(pygame_font.get_default_font(), REGULAR_FONT_SIZE)

        logging_info("Loading Sounds and Music: Working")
        # Game music
        self.game_music_intro = MUSIC_INTRO
        self.game_music_loop = MUSIC_LOOP
        self.playlist = [self.game_music_loop]
        self.current_track = 0
        if self.app.is_audio:
            try:
                pygame_mixer.music.load(self.game_music_intro)
                pygame_mixer.music.set_volume(float(self.app.app_config["settings"]["sound"]["music_volume"]))

                # Game Sounds
                self.sounds = [
                    pygame_mixer.Sound(SOUND_SNAKE_DEATH),
                    pygame_mixer.Sound(SOUND_FOOD_PICKUP),
                    pygame_mixer.Sound(SOUND_PORTAL_ENTER),
                ]
            except pygame_error:
                # default fallback sound
                size = 44100
                sounds = []
                for num in range(3):
                    sound_arr = np.random.randint(-32768, 32767, size=size*2)
                    sound_arr = sound_arr.reshape(size, 2)
                    default_sound = pygame_sndarray.make_sound(sound_arr)
                    sounds.append(default_sound)
                self.menu_sounds = [
                    pygame_mixer.Sound(sounds[0]), # hover
                    pygame_mixer.Sound(sounds[1]), # forward
                    pygame_mixer.Sound(sounds[2]), # backward
                ]

        logging_info("Loading Sounds and Music: Finished")

        # Game object containers
        self.sprite_group: sprite.RenderUpdates[Entity] = sprite.RenderUpdates()
        self.entity_final_scores = {}

        logging_info("Loading Sprites: Working")
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
        logging_info("Loading Sprites: Finished")

        logging_info("Transforming Sprites: Working")
        # Transform the sprite images relative to grid size
        self.transform_all_entity_images()
        logging_info("Transforming Sprites: Finished")

        # AI blackbox
        self.chosen_ai = None

        logging_info("Building pathfinding grid: Working")
        # Pathfinding grid of the game space
        self.grid_width = self.screen_size[WIDTH] // self.grid_size + self.grid_size
        self.grid_height = self.screen_size[HEIGHT] // self.grid_size + self.grid_size
        self.grid = [[Node(x, y) for y in range(self.grid_height)] for x in range(self.grid_width)]
        logging_info("Building pathfinding grid: Finished")

        logging_info("Building Menus: Working")
        # Set the game menus to the app menu object
        self.app.menu.menu_options[MENU_HOME] = lambda: home_menu(self.app.menu)
        self.app.menu.menu_options[MENU_PAUSE] = lambda: pause_menu(self.app.menu)
        self.app.menu.menu_options[MENU_SETTINGS] = lambda: settings_menu(self.app.menu)
        self.app.menu.menu_options[MENU_GAME_OVER] = lambda: game_over_menu(self.app.menu)
        self.app.menu.menu_options[MENU_KEYBINDING] = lambda: keybinding_menu(self.app.menu)
        self.app.menu.menu_options[MENU_GAMEPLAY] = lambda: gameplay_menu(self.app.menu)
        self.app.menu.menu_options[MENU_LEADERBOARD] = lambda: leaderboard_menu(self.app.menu)
        logging_info("Building Menus: Finished")


    def play_loop(self):
        """play

        play does stuff
        """

        # Execute game object actions via parallel threads
        thread_group: list[Thread] = []
        for obj in self.sprite_group:
            if not obj.state == Entity.ALIVE:
                continue

            if self.app.menu.prev_menu in [MENU_HOME, MENU_PAUSE, MENU_GAME_OVER]:
                obj.refresh_draw()

            thread = Thread(target=self._object_actions, args=(obj,))
            thread.start()
            thread_group.append(thread)

        # Wait for threads to finish
        for thread in thread_group:
            thread.join()

        # Only 1 tick to refresh from pause_menu
        if self.app.menu.prev_menu in [MENU_HOME, MENU_PAUSE]:
            self.app.menu.prev_menu = None

        # show the game bar at top of screen
        self.game_bar_display()

        # if the display should be redone with the debug visuals
        if self.app.app_config["settings"]["debug"]["debug_mode"]:

            self.screen.fill(COLOR_WHITE)

            for row in self.grid:
                for node in row:
                    if not node.walkable:
                        draw.rect(self.screen, COLOR_BLACK, (node.x * self.grid_size, node.y * self.grid_size, self.grid_size, self.grid_size))
                    else:
                        draw.rect(self.screen, COLOR_WHITE, (node.x * self.grid_size, node.y * self.grid_size, self.grid_size, self.grid_size), 1)

            for obj in self.sprite_group:
                if "snake" in obj.name:
                    for x, y in obj.path:
                        draw.rect(self.screen, COLOR_BLUE, (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size))
                    draw.rect(self.screen, COLOR_GREEN, (obj.position[0], obj.position[1], self.grid_size, self.grid_size))
                    if obj.target:
                        draw.rect(self.screen, COLOR_RED, (obj.target[0][0], obj.target[0][1], self.grid_size, self.grid_size))


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

        # Clear previous frame render
        self.screen.fill(COLOR_BLACK)

        # Start on a clean slate
        self.clean_up()

        # Check settings
        self.app.settings_checks()

        # Starting variables
        self.app.menu.menu_option = None
        self.app.pause_game_music = False

        # AI blackbox
        self.chosen_ai = DecisionBox(self)

        # Initilize game objects - Order of these objects actually matter
        # Food objects
        num_of_food = self.game_config["settings"]["gameplay"]["num_of_food"]

        if num_of_food <= 0:
            raise OSError("1 or more food is required to play")

        for _ in range(num_of_food):
            self.sprite_group.add(Food(self))

        # teleporter objects
        teleporter_mod = self.game_config["settings"]["gameplay"]["teleporter"]
        if teleporter_mod:
            self.sprite_group.add(TelePortal(self))

        # initilize player character
        is_human_playing = self.game_config["settings"]["gameplay"]["human_player"]
        if is_human_playing:
            player_snake = Snake(self, is_player=True)
            player_snake.speed_mod = self.game_config["settings"]["gameplay"]["player_speed"]
            if player_snake.speed_mod <= 0:
                player_snake.speed_mod = 0.6
            player_snake.is_killable = self.game_config["settings"]["gameplay"]["killable_player"]
            self.sprite_group.add(player_snake)

        # initilize ai characters
        num_ai = self.game_config["settings"]["gameplay"]["num_ai"]
        for _ in range(num_ai):
            enemy_snake = Snake(self, is_player=False)
            enemy_snake.speed_mod = self.game_config["settings"]["gameplay"]["ai_speed"]
            if enemy_snake.speed_mod <= 0:
                enemy_snake.speed_mod = 0.6
            enemy_snake.is_killable = self.game_config["settings"]["gameplay"]["killable_ai"]
            self.sprite_group.add(enemy_snake)


    def clean_up(self):
        """clean_up

        clean_up does stuff
        """

        # Clear previous frame render
        # self.screen.fill(COLOR_BLACK)

        # Game settings
        self.app.pause_game_music = False

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

        # Clear the grid
        self.grid = [[Node(x, y) for y in range(self.grid_height)] for x in range(self.grid_width)]

        # Free unreferenced memory
        gc_collect()


    def quit_game(self):
        """quit_game

        quit_game does stuff
        """
        self.app.running = False


    def unpause(self):
        """unpause

        unpause does stuff
        """

        # Clear previous frame render
        self.screen.fill(COLOR_BLACK)

        self.app.menu.prev_menu = self.app.menu.menu_option
        self.app.menu.menu_option = None
        self.app.pause_game_music = True


    def game_bar_display(self):
        """game_bar_display

        Returns:
            [type]: [description]
        """

        # Clear previous frame obj's location with the game bar color
        game_bar_pos = (X, Y, self.screen_size[WIDTH], self.game_bar_height)
        draw.rect(self.screen, COLOR_GREY_DARK, game_bar_pos)

        game_bar_pos = (X, self.game_bar_height-2, self.screen_size[WIDTH], 2)
        draw.rect(self.screen, COLOR_GREY, game_bar_pos)

        score = 0
        for _, value in self.entity_final_scores.items():
            if value["is_player"]:
                score = value["score"]

        self.app.menu.render_text(f"Score:{score}", .35, -1, color=COLOR_RED, clear_background=False, relative_from="top")


    def transform_all_entity_images(self):
        """transform_all_entity_images

        transform_all_entity_images does stuff
        """

        # Transform the snake's size
        index = 0
        for image in self.snake_images:
            self.snake_images[index] = transform.scale(image, (self.grid_size, self.grid_size))
            index += 1

        # Transform the enemy snake's size
        index = 0
        for image in self.snake_enemy_images:
            self.snake_enemy_images[index] = transform.scale(image, (self.grid_size, self.grid_size))
            index += 1

        # Transform the food's size
        index = 0
        for image in self.food_images:
            self.food_images[index] = transform.scale(image, (self.grid_size, self.grid_size))
            index += 1

        # Transform the teleporters's size
        index = 0
        for image in self.tele_portal_images:
            self.tele_portal_images[index] = transform.scale(image, (self.grid_size, self.grid_size))
            index += 1


def is_multiple_of_4(number):
    """
    Verify if a number is a multiple of 4.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is a multiple of 4, False otherwise.
    """
    return number % 4 == 0