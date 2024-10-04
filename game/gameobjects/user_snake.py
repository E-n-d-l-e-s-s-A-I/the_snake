from .snake import Snake
from .abstaract import UserGameObject
from game.constatnts import *


class UserSnake(Snake, UserGameObject):
    """Class of game objectr snake"""

    _time_to_move = 1
    _color = SNAKE_COLOR
