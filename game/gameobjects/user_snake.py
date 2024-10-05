from .snake import Snake
from .abstaract import UserGameObject
from .abstaract import GameObject
from .rock import Rock
from game.decorators import collision_handler, collision_with_yourself_handler
from game.constatnts import *


class UserSnake(Snake, UserGameObject):
    """Class of game objectr snake"""

    _time_to_move = 1
    _color = SNAKE_COLOR
