from game.constatnts import *
from .gameobject import GameObject


class Apple(GameObject):
    """Class of game objectr appple"""

    def __init__(self, gamefield, *args, **kwargs):
        super().__init__(gamefield=gamefield, color=APPLE_COLOR,
                         *args, **kwargs)
