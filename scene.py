"""
Code to render each type of scene in the game.
"""

from json import load
from abc import ABC, abstractmethod
from ast import literal_eval

from PIL import Image
import pygame

# Pygame window size constants
GLOBAL_WINDOW_WIDTH = 800
GLOBAL_WINDOW_HEIGHT = 500

# External file constants
MAP_SCENES_FILEPATH = "data/scene_data/map.json"
MAP_BACKGROUND_FILEPATH = "data/scene_data/map_final.png"
EVENT_SCENES_FILEPATH = "data/event_data/events.json"

# Pygame font constants
FONT_FILEPATH = "data/fonts/pixel.ttf"
SMALL_FONT_SIZE = 20
WORDS_PER_LINE = 9
LARGE_FONT_SIZE = 48
WHITE = (255, 255, 255)

# Constants related to positioning text within the window
SIDE_EDGE_OFFSET = 10
LINE_OFFSET = 30
BOTTOM_EDGE_OFFSET = 25
MAX_STRING_LENGTH = 280
HEALTH_HEIGHT = 10
INVENTORY_HEIGHT = HEALTH_HEIGHT + (LINE_OFFSET * 2)

# Text constants related to printing directions
DIRECTION_KEY = ["Left <-", "Right ->", "Forward ^", "Down V"]

# Constant messages to print
DEFAULT_DEATH_MESSAGE = "Your health has reached zero."


class Scene(ABC):
    """
    Handles displaying and updating scenes to the player
    """

    def __init__(self, surface, player) -> None:
        """
        Loads the pygame surface that scenes will be displayed on and
        defines the fonts that will be used on text throughout the game

        Args:
            surface: pygame surface representing the surface to draw
            scenes objects on to
            player: PlayerCharacter object to keep track of scene state in
        """
        super().__init__()

        # Load the pygame surface being used
        self._surface = surface

        # Define fonts to be used in drawing a scene
        self._pixel_font_small = pygame.font.Font(
            FONT_FILEPATH, SMALL_FONT_SIZE
        )

        # Define font text colors
        self._white = WHITE
        self._red = (255, 0, 0)
        self._green = (0, 255, 0)

        # Load the player character for later reference (health, inventory, etc)
        #
        # Create a copy of the player using the player_sprite class, which
        # extends the pygame sprite class.
        self._player = player
        self._player_sprite = PlayerSprite(self._player)

    @property
    def surface(self):
        """
        Return the pygame surface being used to draw the scenes onto.

        Returns:
            pygame surface object being drawn on
        """

    @abstractmethod
    def draw(self, location_id):
        """
        Abstract method, template to draw a scene, regardless of type.
        """

    def draw_player(self, width_difference=0, height_difference=0):
        """
        Draw the player sprite onto the screen, given the amount of the map has
        been offset to prevent it from being displayed off the screen that the
        player should be offset by.

        Args:
            width_difference: integer representing width offset in pixels
                Defaults to zero (draws character in center of screen).
            height_difference: integer representing height offset in pixels.
                Defaults to zero (draws character in center of screen).
        """
        self._surface.blit(
            self._player_sprite.image,
            (
                (
                    # The character is drawn in the center of the screen,
                    # while accounting for the size of the sprite itself and
                    # if the window has been shifted due to being too close
                    # to the edge of the map.
                    (GLOBAL_WINDOW_WIDTH / 2)
                    - (self._player_sprite.width / 2)
                    + width_difference
                ),
                (
                    (GLOBAL_WINDOW_HEIGHT / 2)
                    - (self._player_sprite.height / 2)
                    + height_difference
                ),
            ),
        )

    def display_health(self, health):
        """
        Display the player's current health at standard location on the screen

        Args:
            health: integer representing the player's current health
        """
        # Print health in white text
        color = (255, 255, 255)
        health_text = self._pixel_font_small.render(
            f"Health: {health}", True, color
        )
        self._surface.blit(health_text, (SIDE_EDGE_OFFSET, HEALTH_HEIGHT))

    def display_inventory(self, inventory):
        """
        Display the player's current inventory at standard location on the
        screen.

        Args:
            inventory: list of strings representing the player's current
                inventory
        """
        # Print in white font
        color = (255, 255, 255)
        inventory_title_text = self._pixel_font_small.render(
            "Inventory:", True, color
        )
        self._surface.blit(
            inventory_title_text, (SIDE_EDGE_OFFSET, INVENTORY_HEIGHT)
        )
        for index, item in enumerate(inventory):
            inventory_item_text = self._pixel_font_small.render(
                item, True, color
            )
            self._surface.blit(
                inventory_item_text,
                (
                    SIDE_EDGE_OFFSET,  # x cords
                    (INVENTORY_HEIGHT + (LINE_OFFSET * (index + 1))),  # y cords
                ),
            )

    def split_text_to_lines(self, start, direction, text):
        """
        Split text that is too long to fit on the screen into a single line into
        multiple lines and print to surface.

        Based on the input of direction, lines will either be added on top of
        the starting point or below the starting point.

        Args:
            start: tuple of ints (width, height) where first line of text
                should be printed
            direction: boolean with True representing lines above start and
                False below
            text: string representing all text to be printed
        """
        # Multiplier to move in positive or negative direction pixel-wise based
        # on the direction input
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

        # If the text is being printed up from the starting coordinates, then
        # the list of lines needs to be reversed since the text is printed
        # bottom up.
        if direction:
            lines = lines.reverse()

        # Print each line sequentially on the screen
        for index, line in enumerate(lines):
            line_text = self._pixel_font_small.render(line, True, WHITE)
            text_rect = line_text.get_rect(
                center=(
                    start[0],
                    # Each line of text adds a standard amount of spacing
                    # per line to the height
                    start[1] + (index * LINE_OFFSET * direction_multiplier),
                )
            )
            self._surface.blit(line_text, text_rect)


class MapScene(Scene):
    """
    Overall class to draw map type scenes throughout the game. Works based on
    an event ID loaded from the map.json data file.

    Uses one large method to create the entire scene, calling smaller methods
    as it goes through.
    """

    def __init__(self, surface, player) -> None:
        """
        Init. a map scene to be drawn, including taking in the surface to be
        drawn on and taking in a player so that model state information can be
        printed.

        Args:
            surface: pygame Surface object on which to draw
            player: PlayerCharacter object to be drawn onto the surface
        """
        super().__init__(surface, player)

        # Load scene data
        with open(MAP_SCENES_FILEPATH, "r", encoding="utf-8") as datafile:
            self._scene_data = load(datafile)

        # Load the map scene background image
        #
        # Additionally, store the size of the image to later ensure that the
        # screen does not display beyond the edge of the map (this uses pillows)
        self._map_background = pygame.image.load(MAP_BACKGROUND_FILEPATH)
        map_width, map_height = Image.open(MAP_BACKGROUND_FILEPATH).size

        self._map_size = (map_width, map_height)

    @property
    def scene_data(self):
        """
        Return the scene data loaded from the external file.

        Returns:
            Dictionary with string keys and string/integer values representing
                all scene data
        """
        return self._scene_data

    def display_movement_directions(self, next_moves):
        """
        Draw next map move options

        Given a tuple from the scene data in the format
        (left, right, up, down), where each index is either None (representing
        that the player can not move that direction) or an integer
        (representing the player CAN move that direction, and the new scene_id
        that direction would correspond to), print the options the player
        has for movement.

        Args:
            next_moves: tuple of length 4 as described above
        """
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
                    DIRECTION_KEY[index], True, WHITE
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
            "Choose a direction to go: ", True, WHITE
        )
        self._surface.blit(
            move_directions,
            (
                SIDE_EDGE_OFFSET,  # x coords
                GLOBAL_WINDOW_HEIGHT  # y coords - from bottom edge
                - (directions * LINE_OFFSET)  # offset y based on # of direction
                - BOTTOM_EDGE_OFFSET,  # offset y by standard bottom offset
            ),
        )

    def draw_background(
        self, background, image_size, width_center, height_center
    ):
        """
        Draw a background image onto the pygame surface centered around
        specific coordinates of an image.

        If the coordinates are too close to the edge of the image (ie, the image
        won't cover the entire screen if drawn with the given points centered),
        the image is drawn offset and the distance the image had to be drawn
        offset is returned.

        Args:
            background: pygame image object to be drawn as the background
            image_size: tuple of two ints (width, height) of background size
            width_center: integer representing pixel coordinates of image which
                to center in the window (width of image)
            height_center: integer representing pixel coordinates of image which
                to center in the window (height of image)

        Returns:
            A tuple of two integers representing the width and height shift to
                make the image fill the entire screen.
        """

        # Calculate where to center the map around the current point
        width_difference = 0
        height_difference = 0

        map_width_corner = width_center - (GLOBAL_WINDOW_WIDTH / 2)
        map_height_corner = height_center - (GLOBAL_WINDOW_WIDTH / 2)

        # Make sure the point is not going to be too close to the edge of the
        # map such that part of the map will get cut off. If too close to edge,
        # move so the point is not centered.
        if (map_width_corner + GLOBAL_WINDOW_WIDTH) > image_size[0]:
            width_difference = (
                map_width_corner + GLOBAL_WINDOW_WIDTH - image_size[0]
            )
            map_width_corner -= width_difference

        if (map_height_corner + GLOBAL_WINDOW_HEIGHT) > image_size[1]:
            height_difference = (
                map_height_corner + GLOBAL_WINDOW_HEIGHT - image_size[1]
            )
            map_height_corner -= height_difference

        # Actually draw the background
        self._surface.blit(background, (-map_width_corner, -map_height_corner))

        # Return the map offsets
        return (width_difference, height_difference)

    def draw(self, location_id):
        """
        Display the scene of the specified ID in the Pygame window.

        This function prints all necessary information to display a scene,
        including setting the background and displaying directions the player
        can travel and printing player state information like health and
        inventory. The method additionally processes the scene data to
        determine the directions the player can travel and displays appropriate
        instructions.

        Args:
            location_id: integer ID of the scene to be loaded from the map scene
                data file.
        """
        # Load data for the current map point to be displayed
        current_scene = self._scene_data[location_id]

        # Draw background with helper function
        (width_difference, height_difference) = self.draw_background(
            self._map_background,
            self._map_size,
            current_scene["MapPointCenterWidth"],
            current_scene["MapPointCenterHeight"],
        )

        # Draw current player health
        self.display_health(self._player.health)

        # Draw current player inventory
        self.display_inventory(self._player.inventory)

        # Draw character sprite
        self.draw_player(
            width_difference,
            height_difference,
        )

        # Print next movement directions
        #
        # When imported from the JSON data, the tuple gets stored as a string,
        # and the following line converts it back to a tuple.
        next_moves = literal_eval(current_scene["DirectionsToMove"])
        self.display_movement_directions(next_moves)


class EventScene(Scene):
    """
    Overall class to draw all event-type scenes in the game, based on the
    information in the events.json datafile.

    Uses one main method to draw the entire scene, calling upon helper methods
    shared by each map scene class.
    """

    def __init__(self, surface, player):
        super().__init__(surface, player)

        # Load event scene data
        with open(EVENT_SCENES_FILEPATH, "r", encoding="utf-8") as datafile:
            self._scene_data = load(datafile)

        # Define additional fonts to be used for event scenes
        self._pixel_font_large = pygame.font.Font(
            FONT_FILEPATH, LARGE_FONT_SIZE
        )

    def draw(self, location_id):
        # Load data for current even
        event_scene = self._scene_data[location_id]

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
        self.split_text_to_lines(
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 8),
            False,
            event_scene["TextPrompt"],
        )

        # Convert text options into a list
        options = literal_eval(event_scene["TextOptions"])

        # Check for flashlight in three options case
        if len(options) == 3 and not self._player.in_inventory("Flashlight"):
            options = options[1 : len(options)]

        # Convert all text options into one string and display the corresponding
        # keys to press
        options_string = ""
        for index, option in enumerate(options):
            options_string += f"{option} (press {index + 1}), "
        # Remove the final trailing space and comma from the string
        options_string = options_string[0 : len(options_string) - 2]

        # Draw event options onto surface
        self.split_text_to_lines(
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
        self.display_health(self._player.health)

        # Draw current player inventory
        self.display_inventory(self._player.inventory)

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
        # Clear the screen; make a black background
        self._surface.fill((0, 0, 0))

        self.split_text_to_lines(
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 2),
            False,
            death_message,
        )

        died = self._pixel_font_large.render("YOU DIED", True, self._red)
        died_rect = died.get_rect(center=(GLOBAL_WINDOW_WIDTH // 2, 50))

        self._surface.blit(died, died_rect)

    def draw_win_scene(self, win_message):
        """
        Draw a scene telling the player they have won along with the associated
        win message

        Args:
            win_message: string representing the win message to be printed
        """
        self._surface.fill((0, 0, 0))

        self.split_text_to_lines(
            (GLOBAL_WINDOW_WIDTH / 2, GLOBAL_WINDOW_HEIGHT / 2),
            False,
            win_message,
        )

        won = self._pixel_font_large.render("YOU WON!", True, self._green)
        won_rect = won.get_rect(center=(GLOBAL_WINDOW_WIDTH // 2, 50))

        self._surface.blit(won, won_rect)


class PlayerSprite(pygame.sprite.Sprite):
    """
    Turn our player character model object into a sprite object that pygame can
    draw correctly.
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
