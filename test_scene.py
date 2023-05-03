"""
Unit tests to test the functions in the scene class that don't exclusively
print to a pygame surface.

NOTE: THESE UNIT TESTS RELY ON BEING ABLE TO CREATE A PYGAME WINDOW
"""

import pygame
from PIL import Image
import scene
import character


def test_map_no_offset():
    """
    Test that for a map point where the map can be centered at that point
    and cover the entire screen that the offset is zero.
    """
    window_width = 800
    window_height = 500

    # Create surface to be used for testing
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))

    # create dummy player
    player = character.PlayerCharacter("data/sprite_data/resting.png", 10)

    # create map scene object to use to draw background
    map_scene = scene.MapScene(surface, player)

    (width_difference, height_difference) = map_scene.draw_background(
        pygame.image.load(scene.MAP_BACKGROUND_FILEPATH),
        Image.open(scene.MAP_BACKGROUND_FILEPATH).size,
        1400,  # random width towards the center of the map
        900,  # random height towards the center of the map
    )

    # asset no offset has been done to the background
    assert width_difference == 0
    assert height_difference == 0

    pygame.quit()


def test_map_offset():
    """
    Test that for a point too close to the edge of the map (the map wouldn't
    fill the whole screen if centered at that point), there is an appropriate
    offset of the map that is then returned.
    """

    window_width = 800
    window_height = 500

    # distance to offset the corner from
    offset = 1

    (image_width, image_height) = Image.open(scene.MAP_BACKGROUND_FILEPATH).size

    # Create surface to be used for testing
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))

    # create dummy player - 10 is used as a default health value.
    player = character.PlayerCharacter("data/sprite_data/resting.png", 10)
    map_scene = scene.MapScene(surface, player)

    (width_difference, height_difference) = map_scene.draw_background(
        pygame.image.load(scene.MAP_BACKGROUND_FILEPATH),
        (image_width, image_height),
        offset,  # 1 pixel < the total width of the background
        image_height - offset,  # 1 pixel < the total height of the background
    )

    assert width_difference == (window_width // 2) - 1
    assert height_difference == (window_height // 2) - 1

    pygame.quit()


def test_map_offset_opposite_direction():
    """
    Test that for a map that needs to be shifted in the opposite direction that
    the offset is correctly returned.
    """
    window_width = 800
    window_height = 500

    # distance to offset the corner from
    offset = 1

    (image_width, image_height) = Image.open(scene.MAP_BACKGROUND_FILEPATH).size

    # Create surface to be used for testing
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))

    # create dummy player - 10 is used as a default health value.
    player = character.PlayerCharacter("data/sprite_data/resting.png", 10)
    map_scene = scene.MapScene(surface, player)

    (width_difference, height_difference) = map_scene.draw_background(
        pygame.image.load(scene.MAP_BACKGROUND_FILEPATH),
        (image_width, image_height),
        offset,
        offset,
    )

    assert width_difference == (window_width // 2) - 1
    assert height_difference == (window_height // 2) - 1

    pygame.quit()
