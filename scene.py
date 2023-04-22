"""
Code to render each type of scene in the game.
"""

from json import load
from abc import ABC, abstractmethod
from PIL import Image

import pygame
from pygame.locals import *
import pygame_gui

GLOBAL_WINDOW_WIDTH = 800
GLOBAL_WINDOW_HEIGHT = 500

MAP_SCENES_FILEPATH = "data/scene_data/map.json"
MAP_BACKGROUND_FILEPATH = "data/scene_data/map1.png"

FONT_FILEPATH = "data/fonts/pixel.ttf"
SMALL_FONT_SIZE = 20
LARGE_FONT_SIZE = 48


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

        # Calculate where to center the map around the current point
        width_difference = 0
        height_difference = 0

        map_width_corner = current_scene["MapPointCenterWidth"] - (
            GLOBAL_WINDOW_WIDTH / 2
        )
        map_height_corner = current_scene["MapPointCenterHeight"] - (
            GLOBAL_WINDOW_WIDTH / 2
        )

        # Make sure the point is not going to be too close to the edge of the
        # map such that part of the map will get cut off. If too close to edge,
        # move so the point is not centered.
        if (map_width_corner + GLOBAL_WINDOW_WIDTH) > self._map_width:
            width_difference = (
                map_width_corner + GLOBAL_WINDOW_WIDTH - self._map_width
            )
            map_width_corner -= width_difference

        if (map_height_corner + GLOBAL_WINDOW_HEIGHT) > self._map_height:
            height_difference = (
                map_height_corner + GLOBAL_WINDOW_HEIGHT - self._map_height
            )
            map_height_corner -= height_difference

        # Actually draw the background
        self._surface.blit(
            self._map_background, (-map_width_corner, -map_height_corner)
        )

        # Draw current player health
        health_text = self._pixel_font_small.render(
            f"Health: {self._player.health}", True, self._white
        )
        self._surface.blit(health_text, (10, 10))

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
