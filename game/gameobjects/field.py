import pygame

from game.constatnts import *
from .abstaract.gameobject import GameObject
from .abstaract.moveable_game_object import MoveableGameObject


class Field:
    """Gamefield class"""

    def __init__(self, width, height, screen):
        self._static_objects = [[None for _ in range(height)]
                                for _ in range(width)]
        self.gameobjects = []
        self.width = width
        self.height = height
        self.screen = screen

    def add_gameobject(self, cls):
        """Add gameobject to Field"""
        gameobject = cls(gameobjects=self.gameobjects)
        if not isinstance(gameobject, GameObject):
            raise ValueError("not game object")

        if not isinstance(gameobject, MoveableGameObject):
            for position in gameobject.positions:
                self._static_objects[position[0]][position[1]] = gameobject
            gameobject.draw(self.screen)

        self.gameobjects.append(gameobject)
        return gameobject

    def delete_gameobject(self, gameobject):
        """Delete gameobject from Field"""
        self.gameobjects.remove(gameobject)
        gameobject.clear(self.screen)

        if not isinstance(gameobject, MoveableGameObject):
            for position in gameobject.positions:
                self._static_objects[position[0]][position[1]] = None

    def reset(self):
        """Reset Gamefield"""
        for gameobject in self.gameobjects[:]:
            self.delete_gameobject(gameobject)

    def __getitem__(self, index):
        """getitem() realisation"""
        return self._static_objects[index]

    def draw(self):
        """Draw field"""
        for gameobject in self.gameobjects:
            if isinstance(gameobject, MoveableGameObject):
                gameobject.draw(self.screen)

    def __str__(self) -> str:
        """str() realisation"""
        return "\n".join([" ".join(map(str, row))
                          for row in self._static_objects
                          ])
