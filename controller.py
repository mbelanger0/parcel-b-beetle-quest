"""
Take keyboard input to control different scenes within the game.
"""

from abc import ABC, abstractmethod
import pygame
from json import load


key_conversion = {
    pygame.K_LEFT: "Left",
    pygame.K_RIGHT: "Right",
    pygame.K_UP: "Top",
    pygame.K_DOWN: "Down",
}


class Controller(ABC):
    """
    Docstring
    """

    @abstractmethod
    def get_next_move(self, options):
        """
        Abstract method used to determine the key that is pressed which
        will be used to determine the next move in the game
        """

    @abstractmethod
    def find_travel_directions(self, next_directions):
        """
        Abstract method used to determine what direction the player can
        move at each decision point on the map
        """

    @abstractmethod
    def find_result_event(self, event_id, event_data):
        """
        Abstract method to determine what event follows an event decision
        """


class TextController(Controller):
    """
    Docstring
    """

    def get_next_move(self, options):
        """
        Determined what key is pressed down so that the next move
        in the game can be determined

        args:
            options: list of strings representing all of the possible options
            of keys that can be pressed down at a certain location in the game

        returns:
            string representing the key that is pressed
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in options:
                for key in options:
                    if key == event.key:
                        return key

    def find_travel_directions(self, next_direction):
        """
        Determines what direction the player can move at each decision
        point on the map

        Args:
            next_direction: tuple of integers or None
            surface: pygame surface that the game is being displayed on
            width: integer representing the width in pixels of the pygame surface
            height: integer representing the height in pixels of the pygame surface

        Return:
            String telling the possible directions that the player can go
        """
        next_direction[0] = pygame.K_LEFT
        next_direction[1] = pygame.K_RIGHT
        next_direction[2] = pygame.K_UP
        next_direction[3] = pygame.K_DOWN
        directions = []

        # Determining what directions are possible at a point
        for direction, index in enumerate(next_direction):
            if next_direction[index] != None:
                directions.append(key_conversion[direction])
        return "or".join(directions)

    def find_result_event(self, event_id, event_data):
        """
        Determines the resultant of a players decision after an event

        Args:
            event_id: integer representing the current event that the game is at
            event_data: string representing file path to the data of the
            possible events

        Returns:
            integer representing the new event ID for the game to progress to
        """
        moves = [pygame.K_0, pygame.K_1]
        with open(event_data, "r", encoding="utf-8") as datafile:
            self._event_data = load(datafile)
        current_event = self._event_data[event_id]

        decision = self.get_next_move(moves)
        if decision == pygame.K_0:
            return current_event["O1ResultEventID"]
        if decision == pygame.K_1:
            return current_event["O2ResultEventID"]
