"""
Take keyboard input to control different scenes within the game.
"""

from abc import ABC, abstractmethod
import pygame
from json import load
from ast import literal_eval


# Define all possible keys that will be looked for during event sequences. This
# defines the maximum number of options to be displayed.
EVENT_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]


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
        while True:
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
        while True:
            decision = self.get_next_move()
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
        # Load the current event data to determine how many options are possible
        # and what the results of the keypress will be
        current_event = self._event_data[event_id]

        # Based on number of options, determine which keys can be pressed
        moves = EVENT_KEYS[0 : len(literal_eval(current_event["TextOptions"]))]

        # Continue to loop until a correct key is pressed
        while True:
            decision = self.get_next_move()
            for index, key in enumerate(moves):
                if decision == key:
                    return (
                        # In importing to JSON, lists are stored as strings,
                        # and literal_eval converts from the string back into a
                        # list
                        literal_eval(current_event["OptionResultID"])[index],
                        literal_eval(current_event["HealthChange"])[index],
                        literal_eval(current_event["AddInventory"])[index],
                        literal_eval(current_event["GameEnd"])[index],
                        literal_eval(current_event["ItemCheck"])[index]
                    )
