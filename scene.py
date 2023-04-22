"""
Code to render each type of scene in the game.
"""

from json import load
from abc import ABC, abstractmethod
from PIL import Image
from ast import literal_eval

import pygame
from pygame.locals import *

GLOBAL_WINDOW_WIDTH = 800
GLOBAL_WINDOW_HEIGHT = 500

MAP_SCENES_FILEPATH = "data/scene_data/map.json"
MAP_BACKGROUND_FILEPATH = "data/scene_data/map1.png"

FONT_FILEPATH = "data/fonts/pixel.ttf"
SMALL_FONT_SIZE = 20
LARGE_FONT_SIZE = 48

# Constants related to positioning text within the window
SIDE_EDGE_OFFSET = 10
LINE_OFFSET = 30
BOTTOM_EDGE_OFFSET = 25

HEALTH_HEIGHT = 10
INVENTORY_HEIGHT = HEALTH_HEIGHT + (LINE_OFFSET * 2)


# Constants related to printing directions
DIRECTION_KEY = ["Left ->", "Right ->", "Up ^", "Down V"]


class Scene(ABC):
    def __init__(self, surface) -> None:
        super().__init__()

        # Load the pygame surface being used
        self._surface = surface

        # Define fonts to be used in drawing a scene
        self._pixel_font_small = pygame.font.Font(
            FONT_FILEPATH, SMALL_FONT_SIZE
        )
        self._pixel_font_large = pygame.font.Font(
            FONT_FILEPATH, LARGE_FONT_SIZE
        )

        # Define font text colors
        self._white = (255, 255, 255)

    @abstractmethod
    def draw(self, scene_id):
        """
        Abstract method, template to draw a scene, regardless of type.
        """
        pass


class MapScene(Scene):
    def __init__(self, surface, player) -> None:
        """
        Draw a map scene, including displaying the background correctly and
        displaying the character sprite/character health information.

        Args:
            surface: pygame Surface object on which to draw
            player: PlayerCharacter object to be drawn onto the surface
        """
        super().__init__(surface)

        # Load scene data
        with open(MAP_SCENES_FILEPATH, "r", encoding="utf-8") as datafile:
            self._scene_data = load(datafile)

        # Load the map scene background image
        self._map_background = pygame.image.load(MAP_BACKGROUND_FILEPATH)
        self._map_width, self._map_height = Image.open(
            MAP_BACKGROUND_FILEPATH
        ).size

        # Load the player character for later reference
        self._player = player

    def draw(self, scene_id):
        """
        Display the scene of the specified ID in the Pygame window.

        Args:
            scene_id: integer ID of the scene to be loaded from the map scene
                data file.
        """
        # Load data for the current map point to be displayed
        current_scene = self._scene_data[scene_id]

        # Draw background with helper function
        (width_difference, height_difference) = draw_background(
            self._surface,
            self._map_background,
            self._map_width,
            self._map_height,
            current_scene["MapPointCenterWidth"],
            current_scene["MapPointCenterHeight"],
        )

        # Draw current player health
        health_text = self._pixel_font_small.render(
            f"Health: {self._player.health}", True, self._white
        )
        self._surface.blit(health_text, (SIDE_EDGE_OFFSET, HEALTH_HEIGHT))

        # Draw current player inventory
        inventory_title_text = self._pixel_font_small.render(
            "Inventory:", True, self._white
        )
        self._surface.blit(
            inventory_title_text, (SIDE_EDGE_OFFSET, INVENTORY_HEIGHT)
        )
        for index, item in enumerate(self._player.inventory):
            inventory_item_text = self._pixel_font_small.render(
                item, True, self._white
            )
            self._surface.blit(
                inventory_item_text,
                (
                    SIDE_EDGE_OFFSET,  # x cords
                    (INVENTORY_HEIGHT + (LINE_OFFSET * (index + 1))),  # y cords
                ),
            )

        # Draw character sprite
        player_sprite = PlayerSprite(self._player)
        self._surface.blit(
            player_sprite.image,
            (
                (
                    # The character is drawn in the center of the screen,
                    # while accounting for the size of the sprite itself and
                    # if the window has been shifted due to being too close
                    # to the edge of the map.
                    (GLOBAL_WINDOW_WIDTH / 2)
                    - (player_sprite.width / 2)
                    + width_difference
                ),
                (
                    (GLOBAL_WINDOW_HEIGHT / 2)
                    - (player_sprite.height / 2)
                    + height_difference
                ),
            ),
        )

        # Draw next move options
        next_moves = literal_eval(current_scene["DirectionsToMove"])
        directions = 0
        for index, value in enumerate(next_moves):
            if value is not None:
                next_move_text = self._pixel_font_small.render(
                    DIRECTION_KEY[index], True, self._white
                )
                self._surface.blit(
                    next_move_text,
                    (
                        SIDE_EDGE_OFFSET,
                        (
                            GLOBAL_WINDOW_HEIGHT
                            - ((directions * LINE_OFFSET) + BOTTOM_EDGE_OFFSET)
                        ),
                    ),
                )
                directions += 1

        # Render instruction text
        move_directions = self._pixel_font_small.render(
            "Choose a direction to go: ", True, self._white
        )
        self._surface.blit(
            move_directions,
            (
                SIDE_EDGE_OFFSET,  # x coords
                GLOBAL_WINDOW_HEIGHT  # y coords - from bottom edge
                - (directions * LINE_OFFSET)  # offset based on # of directions
                - BOTTOM_EDGE_OFFSET,  # standard bottom offset
            ),
        )

    def move_to_point(self, old_id, new_id, direction):
        """
        Animate movement from one point to another on the map.

        Valid directions of travel are: LEFT, RIGHT, UP, DOWN

        Args:
            old_id: integer id of current map point location
            new_id: integer id of new map point location
            direction: string representing direction of travel
        """
        pass


class EventScene(Scene):
    pass


class PlayerSprite(pygame.sprite.Sprite):
    """
    Turn our player character object into a sprite object that pygame can
    draw.
    """

    def __init__(self, character) -> None:  # , *groups: _Group) -> None:
        """
        Init the sprite by setting the image and boundaries it is contained
        within.

        Args:
            character: PlayerCharacter object to be draw
        """
        super().__init__()  # *groups)
        self._image = pygame.image.load(character.filepath)

        self._width, self._height = Image.open(character.filepath).size

    @property
    def width(self):
        """
        Return the width of the image representing the sprite
        """
        return self._width

    @property
    def height(self):
        """
        Return the height of the image representing the sprite
        """
        return self._height

    @property
    def image(self):
        """
        Return the pygame image object representing the Sprite
        """
        return self._image


def draw_background(
    surface, background, image_width, image_height, width_center, height_center
):
    """
    Draw a background image onto a pygame surface centered around
    specific coordinates of an image.

    If the coordinates are too close to the edge of the image (ie, the image
    won't cover the entire screen if drawn with the given points centered), the
    image is drawn offset and the distance the image had to be drawn offset is
    returned.

    Args:
        surface: pygame surface on which to draw
        background: pygame image object to be drawn as the background
        image_width: integer representing image width in pixels
        image_height: integer representing image height in pixels
        width_center: integer representing pixel coordinates of image which to
            center in the window (width of image)
        height_center: integer representing pixel coordinates of image which to
            center in the window (height of image)

    Returns:
        A tuple of two integers representing the width and height shift to make
            the image fill the entire screen.
    """

    # Calculate where to center the map around the current point
    width_difference = 0
    height_difference = 0

    map_width_corner = width_center - (GLOBAL_WINDOW_WIDTH / 2)
    map_height_corner = height_center - (GLOBAL_WINDOW_WIDTH / 2)

    # Make sure the point is not going to be too close to the edge of the
    # map such that part of the map will get cut off. If too close to edge,
    # move so the point is not centered.
    if (map_width_corner + GLOBAL_WINDOW_WIDTH) > image_width:
        width_difference = map_width_corner + GLOBAL_WINDOW_WIDTH - image_width
        map_width_corner -= width_difference

    if (map_height_corner + GLOBAL_WINDOW_HEIGHT) > image_height:
        height_difference = (
            map_height_corner + GLOBAL_WINDOW_HEIGHT - image_height
        )
        map_height_corner -= height_difference

    # Actually draw the background
    surface.blit(background, (-map_width_corner, -map_height_corner))

    # Return the map offsets
    return (width_difference, height_difference)
