from game.constatnts import *
import pygame
from random import randint


class GameObject:
    """Abstract class of game object"""

    def __init__(self, *, gameobjects=[]):
        self._set_random_position(gameobjects)

    def draw(self, screen):
        """Draw game object"""
        for position in self.positions:
            rect = (pygame.Rect(self._get_screen_position(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, self._color, rect)
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

    @staticmethod
    def _get_random_position():
        """Get random position"""
        return (randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1))

    @staticmethod
    def _round_position(positon):
        """Round snake position"""
        return (abs(positon[0] % GRID_WIDTH),
                abs(positon[1] % GRID_HEIGHT))

    @staticmethod
    def _get_screen_position(position):
        """Translate grid position to screen position"""
        return tuple(GRID_SIZE * x for x in position)

    def __str__(self):
        """Str realization"""
        return f'{self.__class__.__name__} in {self.positions}'
