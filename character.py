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
        self._inventory = []

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
        Subtracts health from the player and returns whether or not the player
        is still alive.

        A negative health can be passed through to add health to the player

        Args:
            damage: integer representing health to be subtracted
        Returns:
            boolean equaling true if the player is still alive (health > 0)
        """
        self._health -= damage
        return self._health > 0

    def update_inventory(self, item):
        """
        Update player's inventory; if item is in it, remove it, or add it
        if it is not already present.

        Args:
            item: string representing item to be added or removed.
        """
        if item in self._inventory:
            self._inventory.remove(item)
        else:
            self._inventory.append(item)

    def in_inventory(self, item):
        """
        Check if a given item is in a player's inventory.

        Args:
            item: string representing item name
        Returns:
            boolean whether or not item is present in inventory
        """
        return item in self._inventory
