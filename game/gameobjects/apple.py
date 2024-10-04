from game.constatnts import *
from .abstaract import StaticGameObject


class Apple(StaticGameObject):
    """Class of game objectr appple"""

    _color = APPLE_COLOR

    def __init__(self, gameobjects, *args, **kwargs):
        super().__init__(gameobjects=gameobjects, *args, **kwargs)
