"""
Contains all classes for implementing characters (player, enemies, etc) inside
of the game.
"""

from abc import ABC, abstractmethod


class Character(ABC):
    """
    Docstring
    """

    def __init__(self, sprite_path):
        self._sprite_path = sprite_path


class EventCharacter(Character):
    """
    Docstring
    """

    def __init__(self, sprite_path, location):
        """
        Docstring
        """
        super().__init__(sprite_path)
        self._location = location


class PlayerCharacter(Character):
    """
    Docstring
    """

    def __init__(self, sprite_path):
        super().__init__(sprite_path)
        self._sprite_path = sprite_path
        self._health = 100  # can be changed later

    @property
    def health(self):
        """
        Docstring
        """
        return self._health

    @property
    def filepath(self):
        """
        Docstring
        """
        return self._sprite_path

    def update_health(self, damage):
        """
        Docstring
        """
        self._health -= damage
