"""
Code to render each type of scene in the game.
"""

from json import load
from abc import ABC, abstractmethod
from PIL import Image

import pygame
from pygame.locals import *

GLOBAL_WINDOW_WIDTH = 800
GLOBAL_WINDOW_HEIGHT = 500

MAP_SCENES_FILEPATH = "data/scenes/map.json"
MAP_BACKGROUND_FILEPATH = "data/scenes/map1.png"


class Scene(ABC):
    def __init__(self, surface) -> None:
        super().__init__()

        # Load the pygame surface being used
        self._surface = surface

    @abstractmethod
    def draw(self, scene_id):
        """
        Abstract method, template to draw a scene, regardless of type.
        """
        pass


class MapScene(Scene):
    def __init__(self, player, surface) -> None:
        """
        Load general data for all map scenes, player character in order to
        display, and the pygame surface to draw on.

        Args:
            player: PlayerCharacter object to be later drawn on the screen.
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
            scene_id: integer ID of the scene to be loaded.
        """
        # Load data for the current map point to be displayed
        current_scene = self._scene_data[scene_id]

        # Calculate where to center the map around the current point
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
            map_width_corner -= (
                map_width_corner + GLOBAL_WINDOW_WIDTH - self._map_width
            )

        if (map_height_corner + GLOBAL_WINDOW_HEIGHT) > self._map_height:
            map_height_corner -= (
                map_height_corner + GLOBAL_WINDOW_HEIGHT - self._map_height
            )

        # Actually draw the background
        self._surface.blit(
            self._map_background, (-map_width_corner, -map_height_corner)
        )


class EventScene(Scene):
    pass
