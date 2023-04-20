"""
Take keyboard input to control different scenes within the game.
"""

from abc import ABC, abstractmethod
import pygame


class Controller(ABC):
    """
    Docstring
    """

    @abstractmethod
    def get_next_move(self, options):
        """
        Docstring
        """


class TextController(Controller):
    """
    Docstring
    """

    def get_next_move(self, options):
        """
        Docstring
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in options:
                for key in options:
                    if key == event.key:
                        return key
