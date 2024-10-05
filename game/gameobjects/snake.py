from random import choice
import pygame

from .abstaract import GameObject
from .abstaract import MoveableGameObject
from .apple import Apple
from .rock import Rock
from game.decorators import collision_handler, collision_with_yourself_handler
from game.constatnts import *


class Snake(MoveableGameObject):
    """Class of game object snake"""

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
        self.positions = [self.get_head_position()]

    def get_head_position(self):
        """Get position og snake head"""
        return self.positions[0]

    def _shorten_snake(self):
        """Shorten snake if it need"""
        if self.current_lenght == self.length:
            self.tail.append(self.positions.pop())
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
        """Move snake implementation"""
        next_head_postion = self._get_next_head_position()
        self._lengthen_snake(next_head_postion)
        self._shorten_snake()

    @collision_handler(Apple)
    def solve_collision_with_apple(self, apple, game):
        """Collision with apple handler"""
        self.current_lenght += 1
        game._delete_game_object(apple)
        game._create_game_object(Apple)

    @collision_handler(Rock)
    def solve_collision_with_rock(self, rock, game):
        """Collision with rock handler"""
        game._delete_game_object(self)

    @collision_with_yourself_handler
    def solve_collision_with_snake(self, snake, game):
        """Collision with yourself handler"""
        if (self.get_head_position() in snake.positions
                and not snake.get_head_position() in self.positions):
            game._delete_game_object(self)

        elif (snake.get_head_position() in self.positions
                and not self.get_head_position() in snake.positions):
            game._delete_game_object(snake)

        else:
            if game._user_snake is self:
                game._delete_game_object(self)
                return
            elif game._user_snake is snake:
                game._delete_game_object(snake)
                return
            else:
                game._delete_game_object(snake)
                game._delete_game_object(self)
