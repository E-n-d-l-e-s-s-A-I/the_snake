import pygame

from game.constatnts import *
from .abstaract.gameobject import GameObject
from .abstaract.moveable_game_object import MoveableGameObject
from .abstaract.static_game_object import StaticGameObject


class Field:
    """Game field class"""

    def __init__(self, width, height, screen):
        self.objects_field = [[None for _ in range(height)]
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

        for position in gameobject.positions:
            self.objects_field[position[0]][position[1]] = gameobject

        self.gameobjects.append(gameobject)
        gameobject.draw(self.screen)
        return gameobject

    @property
    def static_gameobjects(self):
        """Get static gameobjects"""
        return filter(lambda x: isinstance(x, StaticGameObject),
                      self.gameobjects)

    @property
    def moveable_gameobjects(self):
        """Get moveable gameobjects"""
        return filter(lambda x: isinstance(x, MoveableGameObject),
                      self.gameobjects)

    def delete_gameobject(self, gameobject):
        """Delete gameobject from Field"""
        self.gameobjects.remove(gameobject)

        for position in gameobject.positions[:]:
            if self.objects_field[position[0]][position[1]] is gameobject:
                self.objects_field[position[0]][position[1]] = None
            elif self.objects_field[position[0]][position[1]] is not None:
                gameobject.positions.remove(position)

        if isinstance(gameobject, MoveableGameObject):
            for position in gameobject.tail:
                if self.objects_field[position[0]][position[1]] is gameobject:
                    self.objects_field[position[0]][position[1]] = None
                elif self.objects_field[position[0]][position[1]] is not None:
                    gameobject.tail.remove(position)

        gameobject.clear(self.screen)

    def _clear_tails(self):
        """Clear tail oa all moveable gameobjects"""
        for moveable in self.moveable_gameobjects:
            for position in moveable.tail:
                self.objects_field[position[0]][position[1]] = None

    def update_moveable(self):
        """Update field"""
        self._clear_tails()
        for moveable in self.moveable_gameobjects:

            for position in moveable.positions:
                object_on_position = self.objects_field[position[0]][position[1]]
                if object_on_position and object_on_position is not moveable:
                    raise CollisionException(moveable, object_on_position)
                else:
                    self.objects_field[position[0]][position[1]] = moveable

    def reset(self):
        """Reset Gamefield"""
        for gameobject in self.gameobjects[:]:
            self.delete_gameobject(gameobject)

    def __getitem__(self, index):
        """getitem() implementation"""
        return self.objects_field[index]

    def draw(self):
        """Draw field"""
        for gameobject in self.gameobjects:
            if isinstance(gameobject, MoveableGameObject):
                gameobject.draw(self.screen)


class CollisionException(Exception):
    """Class of collision exception"""

    def __init__(self, game_obj1, game_obj2, *args, **kwargs):
        self.game_obj1 = game_obj1
        self.game_obj2 = game_obj2
        return super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Str"""
        return f'collision f{self.game_obj1} with f{self.game_obj2}'
