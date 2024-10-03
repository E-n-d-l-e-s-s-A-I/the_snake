from random import choice
import pygame

from .moveable_gameobject import MoveableGameobject
from game.constatnts import *

class Snake(MoveableGameobject):
    """Class of game objectr snake"""

    def __init__(self, gamefield, *args, **kwargs):
        super().__init__(gamefield=gamefield, unique=True, cls=self.__class__,
                         color=SNAKE_COLOR, *args, **kwargs)
        self._reset()

    def _reset(self):
        """Reset snake to default"""
        self.length = 1
        self.current_lenght = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.last = None
        self.positions = [self.get_head_position()]

    def get_head_position(self):
        """Get position og snake head"""
        return self.positions[0]

    def _shorten_snake(self):
        """Sgorten snake if it need"""
        if self.current_lenght == self.length:
            self.last = self.positions.pop()
        else:
            self.length += 1

    def _lengthen_snake(self, next_head_postion):
        """Lengthen snake if it need"""
        if next_head_postion in self.positions:
            raise SnakeEatYourselfException
        self.positions.insert(0, next_head_postion)

    def _get_next_head_position(self):
        """Get next head position"""
        next_head_postion = self.get_head_position()
        next_head_postion = tuple(a + b for a, b in
                                  zip(next_head_postion, self.direction))
        next_head_postion = self._round_position(next_head_postion)
        return next_head_postion

    def move(self):
        """Move snake"""
        next_head_postion = self._get_next_head_position()

        self._lengthen_snake(next_head_postion)
        self._shorten_snake()

    def _clear_tail(self, screen):
        if self.last:
            last_rect = pygame.Rect(self._get_screen_position(self.last),
                                    (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def draw(self, screen):
        """Extend draw for snake"""
        super().draw(screen)
        self._clear_tail(screen)

    def clear(self, screen):
        """Extend clear for snake"""
        super().clear(screen)
        self._clear_tail(screen)

    @staticmethod
    def _round_position(positon):
        """Round snake position"""
        return (abs(positon[0] % GRID_WIDTH),
                abs(positon[1] % GRID_HEIGHT))


class SnakeEatYourselfException(Exception):
    """Exception caused when a snake eats yourself"""
