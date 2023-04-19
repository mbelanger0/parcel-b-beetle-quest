"""
Code to render each type of scene in the game.
"""

from abc import ABC, abstractmethod


class Scene(ABC):
    pass


class MapScene(Scene):
    pass


class EventScene(Scene):
    pass
