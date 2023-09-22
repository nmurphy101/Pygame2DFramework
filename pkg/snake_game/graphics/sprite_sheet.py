#!/usr/bin/env python3

"""
    SpriteSheet

    Handling of sprite sheets for the game

    :copyright: (c) 2021 by Nicholas Murphy.
    :license: GPLv3, see LICENSE for more details.
"""


from pygame import (
    image,
    Rect,
    Surface,
    RLEACCEL,
)


class SpriteSheet:
    """SpriteSheet

    Definition of the image/surface
    """

    def __init__(self, filename, debug=False):
        """Load the sheet."""

        self.debug = debug

        try:
            self.sheet = image.load(filename).convert()

        except FileNotFoundError as error:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(error) from error


    def image_at(self, rect, colorkey = None):
        """Load a specific image from a specific rectangle."""

        # Loads image from x, y, x+offset, y+offset.
        rect = Rect(rect)
        image_surf = Surface(rect.size).convert()
        image_surf.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image_surf.get_at((0,0))

            image_surf.set_colorkey(colorkey, RLEACCEL)

        return image_surf


    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""

        return [self.image_at(rect, colorkey) for rect in rects]


    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""

        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]

        return self.images_at(tups, colorkey)


    def load_grid_images(self, num_rows_columns=(0, 0), margin_x_y=(0, 0), padding_x_y=(0, 0)):
        """Load a grid of images.

        x_margin is space between top of sheet and top of first row.
        x_padding is space between rows.
        Assumes symmetrical padding on left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y_pos.
        x_sprite_size = (sheet_width - 2 * margin_x_y[0] - (num_rows_columns[1] - 1) * padding_x_y[0]) / num_rows_columns[1]
        y_sprite_size = (sheet_height - 2 * margin_x_y[1] - (num_rows_columns[0] - 1) * padding_x_y[1]) / num_rows_columns[0]

        sprite_rects = []
        for row_num in range(num_rows_columns[0]):
            for col_num in range(num_rows_columns[1]):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y_pos.
                x_pos = margin_x_y[0] + col_num * (x_sprite_size + padding_x_y[0])
                y_pos = margin_x_y[1] + row_num * (y_sprite_size + padding_x_y[1])
                sprite_rect = (x_pos, y_pos, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects)

        if self.debug:
            print(f"Loaded {len(grid_images)} grid images.")

        return grid_images
