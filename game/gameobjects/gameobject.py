from game.constatnts import *
import pygame
from random import randint


class GameObject:
    """Abstract class of game object"""

    def __init__(self, *, gamefield, unique=False, cls=None, color=None,):

        if unique and list(filter(lambda x: isinstance(x, cls),
                                  gamefield.gameobjects)):
            raise ValueError("unique GameObject already exists")

        self.body_color = color
        self.gamefield = gamefield
        self._set_random_position(gamefield.gameobjects)
        self.gamefield.add_gameobject(self)

    @staticmethod
    def _get_screen_position(position):
        """Translate grid position to screen position"""
        return tuple(GRID_SIZE * x for x in position)

    def draw(self, screen):
        """Draw game object"""
        for position in self.positions:
            rect = (pygame.Rect(self._get_screen_position(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def clear(self, screen):
        """Clear gameobject from screen"""
        for position in self.positions:
            rect = (pygame.Rect(self._get_screen_position(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def _set_random_position(self, gameobjects):
        """Set random position without collisions"""
        position = self._get_random_position()
        while position in list(map(lambda x: x.positions, gameobjects)):
            position = self._get_random_position()

        self.positions = [position]

    def delete(self):
        """Delete object from gamefield"""
        self.gamefield.delete_gameobject(self)
        self.clear(self.gamefield.screen)

    @staticmethod
    def _get_random_position():
        """Get random position"""
        return (randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1))

    def __str__(self):
        """Str realization"""
        return f'{self.__class__.__name__} in {self.positions}'
