"""
Contains all classes for implementing characters (player, enemies, etc) inside
of the game.
"""

from abc import ABC, abstractmethod


class Character(ABC):
    """
    Abstract class used to implement classes for the player character
    and the characters in the events
    """

    def __init__(self, sprite_path, health):
        """
        Determine file path to the sprite image that will represent a character
        and the character health.

        Args:
            sprite_path: string filepath to image file
            health: integer representing default health
        """
        self._sprite_path = sprite_path
        self._health = health

    @property
    def filepath(self):
        """
        Get the sprite image filepath.

        Returns:
            string representing filepath to sprite image file
        """
        return self._sprite_path

    @property
    def health(self):
        """
        Return current player health

        Return:
            integer less than 10 representing the current health
            of the player
        """
        return self._health

    @abstractmethod
    def update_health(self, damage):
        """
        Abstract method to update player's health based on a given damage value.

        Args:
            damage: integer damage value to be subtracted from health
        """


class PlayerCharacter(Character):
    """
    Class to track the location, health, and inventory state of the player
    """

    def __init__(self, sprite_path, health):
        """
        Set character's sprite image and default health.

        Args:
            sprite: sprite_path: string representing the file path to the image
            of the player character sprite
            health: integer representing default health.
        """
        super().__init__(sprite_path, health)
        self._inventory = []

    @property
    def inventory(self):
        """
        Return current player inventory

        Returns:
            List of strings representing current inventory
        """
        return self._inventory

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

        Converts all objects being added to the inventory into strings
        for ease of printing later.

        Args:
            item: string representing item to be added or removed.
        """
        if item in self._inventory:
            self._inventory.remove(item)
        else:
            self._inventory.append(str(item))

    def in_inventory(self, item):
        """
        Check if a given item is in a player's inventory.

        Args:
            item: string representing item name
        Returns:
            boolean whether or not item is present in inventory
        """
        return item in self._inventory
