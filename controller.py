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

    def __init__(self, event_data):
        """
        Opens the data file of the data for the events that can happen during game play

        args:
            event_data: string representing file path to the event data
        """
        with open(event_data, "r", encoding="utf-8") as datafile:
            self._event_data = load(datafile)

    def get_next_move(self):
        """
        Determined what key is pressed down at a moment in the game

        returns:
            pygame key object representing the current key that is being pressed down
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

    def find_result_map(self, next_direction):
        """
        Determines what direction the player can move at each decision
        point on the map

        Args:
            next_direction: tuple of integers or None

        Return:
            integer representing the map ID to progress to
        """
        decision = self.get_next_move(next_direction)
        if decision == pygame.K_LEFT and next_direction[0] != None:
            return next_direction[0]
        if decision == pygame.K_RIGHT and next_direction[1] != None:
            return next_direction[1]
        if decision == pygame.K_UP and next_direction[2] != None:
            return next_direction[2]
        if decision == pygame.K_DOWN and next_direction[3] != None:
            return next_direction[3]

    def find_result_event(self, event_id):
        """
        Determines the resultant of a players decision after an event

        Args:
            event_id: integer representing the current event that the game is at

        Returns:
            integer representing the new event ID for the game to move to
            integer representing character health change
            string representing item to be toggled from character inventory
            string representing a game outcome message
            tuple (string, int) with inventory modifier information
        """
        moves = [pygame.K_0, pygame.K_1]
        current_event = self._event_data[event_id]
        decision = self.get_next_move(moves)
        if decision == pygame.K_0:
            return (
                current_event["O1ResultEventID"],
                current_event["O1HealthChange"],
                current_event["O1AddInventory"],
                current_event["O1GameEnd"],
                current_event["ItemCheck"],
            )
        if decision == pygame.K_1:
            return (
                current_event["O2ResultEventID"],
                current_event["O2HealthChange"],
                current_event["O2AddInventory"],
                current_event["O2GameEnd"],
                current_event["ItemCheck"],
            )
