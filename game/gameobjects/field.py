import pygame

from game.constatnts import *
from .gameobject import GameObject
from .moveable_gameobject import MoveableGameobject


class Field:
    """Gamefield class"""

    def __init__(self, width, height, screen):
        self._static_objects = [[None for _ in range(height)] for _ in range(width)]
        self.gameobjects = []
        self.width = width
        self.height = height
        self.screen = screen

    def reset(self):
        """Reset Gamefield"""
        for gameobject in self.gameobjects[:]:
            gameobject.delete()

    def add_gameobject(self, gameobject):
        """Add gameobject to Field"""
        if not isinstance(gameobject, GameObject):
            raise ValueError("not gameobject")

        if not isinstance(gameobject, MoveableGameobject):
            for position in gameobject.positions:
                self._static_objects[position[0]][position[1]] = gameobject
            gameobject.draw(self.screen)

        self.gameobjects.append(gameobject)

    def delete_gameobject(self, gameobject):
        """Delete gameobject from Field"""
        self.gameobjects.remove(gameobject)

        if not isinstance(gameobject, MoveableGameobject):
            for position in gameobject.positions:
                self._static_objects[position[0]][position[1]] = None

    def __getitem__(self, index):
        """getitem() realisation"""
        return self._static_objects[index]

    def draw(self):
        """Draw field frame"""
        for gameobject in self.gameobjects:
            if isinstance(gameobject, MoveableGameobject):
                gameobject.draw(self.screen)

    def __str__(self) -> str:
        """str() realisation"""
        return "\n".join([" ".join(map(str, row))
                          for row in self._static_objects
                          ])
