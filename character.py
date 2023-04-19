"""
Contains all classes for implementing characters (player, enemies, etc) inside
of the game.
"""

from abc import ABC, abstractmethod


class Character(ABC):
    pass


class EventCharacter(Character):
    pass


class PlayerCharacter(Character):
    pass
