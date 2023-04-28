"""
Code to render each type of scene in the game.
"""

from json import load
from abc import ABC, abstractmethod
from PIL import Image
from ast import literal_eval

import pygame
from pygame.locals import *
from character import PlayerCharacter

GLOBAL_WINDOW_WIDTH = 800
GLOBAL_WINDOW_HEIGHT = 500

MAP_SCENES_FILEPATH = "data/scene_data/map.json"
MAP_BACKGROUND_FILEPATH = "data/scene_data/map1.png"
EVENT_SCENES_FILEPATH = "data/event_data/events.json"

FONT_FILEPATH = "data/fonts/pixel.ttf"
SMALL_FONT_SIZE = 20
WORDS_PER_LINE = 9
LARGE_FONT_SIZE = 48

# Constraint for whether or not to display sprites
MAX_STRING_LENGTH = 280

# Constants related to positioning text within the window
SIDE_EDGE_OFFSET = 10
LINE_OFFSET = 30
BOTTOM_EDGE_OFFSET = 25

HEALTH_HEIGHT = 10
INVENTORY_HEIGHT = HEALTH_HEIGHT + (LINE_OFFSET * 2)

# Text Color Constants
WHITE = (255, 255, 255)


# Constants related to printing directions
DIRECTION_KEY = ["Left <-", "Right ->", "Up ^", "Down V"]

# Constant prints
DEFAULT_DEATH_MESSAGE = "Your health has reached zero."


class Scene(ABC):
    """
    Handles displaying and updating scenes to the player
    """

    def __init__(self, surface) -> None:
        """
        Loads the pygame surface that scenes will be displayed on and
        defines the fonts that will be used on text throughout the game

        Args:
            surface: pygame surface representing the surface to draw
            scenes objects on to
        """
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
        self._white = WHITE
        self._red = (255, 0, 0)
        self._green = (0, 255, 0)

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
        #
        # Additionally, store the size of the image to later ensure that the
        # screen does not display beyond the edge of the map
        self._map_background = pygame.image.load(MAP_BACKGROUND_FILEPATH)
        self._map_width, self._map_height = Image.open(
            MAP_BACKGROUND_FILEPATH
        ).size

        # Load the player character for later reference
        self._player = player

    @property
    def scene_data(self):
        """
        Return the scene data loaded from the external file.

        Returns:
            Dictionary with string keys and string/integer values
        """
        return self._scene_data

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
        display_health(
            self._surface,
            self._pixel_font_small,
            self._player.health,
            SIDE_EDGE_OFFSET,
            HEALTH_HEIGHT,
        )

        # Draw current player inventory
        display_inventory(
            self._surface,
            self._pixel_font_small,
            self._player.inventory,
            SIDE_EDGE_OFFSET,
            INVENTORY_HEIGHT,
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
        #
        # Given a tuple from the scene data in the format
        # (left, right, up, down), where each index is either None (representing
        # that the player can not move that direction) or an integer
        # (representing the player CAN move that direction, and the new scene_id
        # that direction would correspond to), print the options the player
        # has for movement.
        #
        # When imported from the JSON data, the tuple gets stored as a string,
        # and the following line converts it back to a tuple.
        next_moves = literal_eval(current_scene["DirectionsToMove"])
        # Keep track of the number of directions for the purpose of positioning
        # new lines of text
        directions = 0
        for index, value in enumerate(next_moves):
            # If the value is not None - the player can move that direction, so
            # print the direction corresponding to that index in the tuple
            # (left, right, up, down)
            if value is not None:
                # Render the corresponding text and display it on the surface
                next_move_text = self._pixel_font_small.render(
                    DIRECTION_KEY[index], True, self._white
                )
                self._surface.blit(
                    next_move_text,
                    (
                        # Print the standard distance from the edge and move
                        # line-by-line up from the bottom left corner of the
                        # screen.
                        SIDE_EDGE_OFFSET,
                        (
                            GLOBAL_WINDOW_HEIGHT
                            - ((directions * LINE_OFFSET) + BOTTOM_EDGE_OFFSET)
                        ),
                    ),
                )
                directions += 1

        # Render instruction text for directions based on the number of lines
        # already printed (the number of directions the player can move)
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
    def __init__(self, surface, player):
        """ """
        super().__init__(surface)
        self._surface = surface
        self._player = player

        # Load event scene data
        with open(EVENT_SCENES_FILEPATH, "r", encoding="utf-8") as datafile:
            self._scene_data = load(datafile)

    def draw(self, event_id):
        # Load data for current even
        event_scene = self._scene_data[event_id]

        if event_scene["BackgroundImage"] != "":
            # Load event background image
            event_background = pygame.image.load(event_scene["BackgroundImage"])
            # Draw background
            self._surface.blit(event_background, (0, 0))
        else:
            self._surface.fill((0, 0, 0))

        # Load and draw event character image
        if event_scene["PromptImage"] != "":
            event_character = pygame.image.load(event_scene["PromptImage"])
            self._surface.blit(
                event_character,
                (4 * GLOBAL_WINDOW_WIDTH / 5, GLOBAL_WINDOW_HEIGHT / 2),
            )

        # Draw text prompt onto surface
        split_text_to_lines(
            self._surface,
            self._pixel_font_small,
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 8),
            False,
            event_scene["TextPrompt"],
        )

        # Convert text options into a list
        options = literal_eval(event_scene["TextOptions"])

        # Check for flashlight in three options case
        if len(options) == 3 and PlayerCharacter(
            "data/sprite_data/resting.png"
        ).in_inventory("Flashlight"):
            options = options[1 : len(options)]

        # Convert all text options into one string and display the corresponding
        # keys to press
        options_string = ""
        for index, option in enumerate(options):
            options_string += f"{option} (press {index + 1}), "
        # Remove the final trailing space and comma from the string
        options_string = options_string[0 : len(options_string) - 2]

        # Draw event options onto surface
        split_text_to_lines(
            self._surface,
            self._pixel_font_small,
            (GLOBAL_WINDOW_WIDTH / 2, 21 * GLOBAL_WINDOW_HEIGHT / 24),
            False,
            options_string,
        )

        # Draw character sprite
        # Don't draw sprites when most of the window is text
        if len(event_scene["TextPrompt"]) < MAX_STRING_LENGTH:
            player_sprite = PlayerSprite(self._player)
            player_sprite_rect = player_sprite.image.get_rect(
                center=(GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 2)
            )
            self._surface.blit(player_sprite.image, player_sprite_rect)

        # Draw current player health
        display_health(
            self._surface,
            self._pixel_font_small,
            self._player.health,
            SIDE_EDGE_OFFSET,
            HEALTH_HEIGHT,
        )

        # Draw current player inventory
        display_inventory(
            self._surface,
            self._pixel_font_small,
            self._player.inventory,
            SIDE_EDGE_OFFSET,
            INVENTORY_HEIGHT,
        )

    @property
    def scene_data(self):
        """
        Return the scene data loaded from the external file.

        Returns:
            Dictionary with string keys and string/integer values
        """
        return self._scene_data

    def draw_death_scene(self, death_message=DEFAULT_DEATH_MESSAGE):
        """
        Draw a scene telling the character they have died, and if applicable,
        the specific death message associated with their choice.

        Args:
            death_message: string representing the death message to be printed.
                Defaults to a message that you're out of health.
        """
        # TODO: deal with multiline text here
        self._surface.fill((0, 0, 0))

        #        death_text = self._pixel_font_small.render(
        #            death_message, True, self._white
        #        )
        #        death_rect = death_text.get_rect(center=(GLOBAL_WINDOW_WIDTH // 2, 300))
        split_text_to_lines(
            self._surface,
            self._pixel_font_small,
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 2),
            False,
            death_message,
        )

        died = self._pixel_font_large.render("YOU DIED", True, self._red)
        died_rect = died.get_rect(center=(GLOBAL_WINDOW_WIDTH // 2, 50))

        # self._surface.blit(death_text, death_rect)
        self._surface.blit(died, died_rect)

    def draw_win_scene(self, win_message):
        """
        Draw a scene telling the player they have won along with the associated
        win message

        Args:
            win_message: string representing the win message to be printed
        """
        self._surface.fill((0, 0, 0))

        split_text_to_lines(
            self._surface,
            self._pixel_font_small,
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 2),
            False,
            win_message,
        )

        won = self._pixel_font_large.render("YOU WON!", True, self._green)
        won_rect = won.get_rect(center=(GLOBAL_WINDOW_WIDTH // 2, 50))

        self._surface.blit(won, won_rect)


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

        Returns:
            integer representing the width of the sprite
        """
        return self._width

    @property
    def height(self):
        """
        Return the height of the image representing the sprite

        Returns:
            integer representing the height of the sprite
        """
        return self._height

    @property
    def image(self):
        """
        Return the pygame image object representing the Sprite

        Returns:
            pygame image object representing the Sprite
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


def display_health(surface, font, health, width, height):
    """
    Display the player's current health at a given location on the screen

    Args:
        surface: pygame surface to draw on
        health: integer representing the player's current health
        font: pygame font to print using
        width_start: integer representing the width pixel location where the
            text is printed
        height_start: integer representing the height pixel location where the
            text is printed
    """
    # Print health in white text
    color = (255, 255, 255)
    health_text = font.render(f"Health: {health}", True, color)
    surface.blit(health_text, (width, height))


def display_inventory(surface, font, inventory, width, height):
    """
    Display the player's current inventory at a given location on the screen.

    Args:
        surface: pygame surface to draw on
        inventory: list of strings representing the player's current inventory
        font: pygame font to print using
        width_start: integer representing the width pixel location where the
            text is printed
        height_start: integer representing the height pixel location where the
            text is printed
    """
    # Print in white font
    color = (255, 255, 255)
    inventory_title_text = font.render("Inventory:", True, color)
    surface.blit(inventory_title_text, (SIDE_EDGE_OFFSET, INVENTORY_HEIGHT))
    for index, item in enumerate(inventory):
        inventory_item_text = font.render(item, True, color)
        surface.blit(
            inventory_item_text,
            (
                width,  # x cords
                (height + (LINE_OFFSET * (index + 1))),  # y cords
            ),
        )


def split_text_to_lines(surface, font, start, direction, text):
    """
    Split text that is too long to fit on the screen into a single line into
    multiple lines and print to surface.

    Based on the input of direction, lines will either be added on top of the
    starting point or below the starting point.

    Args:
        surface: pygame surface on which to print text
        font: pygame font to print text using
        start: tuple of ints (width, height) where first line of text
            should be printed
        direction: boolean with True representing lines above start and False
            below
        text: string representing all text to be printed
    """
    # Multiplier to move in positive or negative direction pixel-wise based on
    # the direction input
    if direction:
        direction_multiplier = -1
    else:
        direction_multiplier = 1

    text_split = text.split(" ")
    lines = []

    # Split the text into lines WORDS_PER_LINE words long
    while len(text_split) > WORDS_PER_LINE:
        words = " ".join(text_split[0:WORDS_PER_LINE])
        lines.append(words)
        text_split = text_split[WORDS_PER_LINE : len(text_split)]

    # Append the line shorter than number per line or the entire thing if
    # shorter than the number per line to the split text
    lines.append(" ".join(text_split[0 : len(text_split)]))

    # If the text is being printed up from the starting coordinates, then the
    # list of lines needs to be reversed since the text is printed bottom up.
    if direction:
        lines = lines.reverse()

    # Print each line sequentially on the screen
    for index, line in enumerate(lines):
        line_text = font.render(line, True, WHITE)
        text_rect = line_text.get_rect(
            center=(
                start[0],
                # Each line of text adds a standard amount of spacing
                # per line to the height
                start[1] + (index * LINE_OFFSET * direction_multiplier),
            )
        )
        surface.blit(line_text, text_rect)
