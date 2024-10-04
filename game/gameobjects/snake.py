from random import choice
import pygame

from .abstaract import UserGameObject
from .abstaract import MoveableGameObject
from game.constatnts import *


class Snake(MoveableGameObject):
    """Class of game objectr snake"""

    _time_to_move = 2
    _distane_to_turn = 10
    _color = ENEMY_SNAKE_COLOR

    def __init__(self, gameobjects, *args, **kwargs):
        super().__init__(gameobjects=gameobjects, *args, **kwargs)
        self._reset()

    def _reset(self):
        """Reset snake to default"""
        self.length = 1
        self.current_lenght = 1
        self._direction = choice([RIGHT, LEFT, UP, DOWN])
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
        self.positions.insert(0, next_head_postion)

    def _get_next_head_position(self):
        """Get next head position"""
        next_head_postion = self.get_head_position()
        next_head_postion = tuple(a + b for a, b in
                                  zip(next_head_postion, self._direction))
        next_head_postion = self._round_position(next_head_postion)
        return next_head_postion

    def _move(self):
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
