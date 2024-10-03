from game.constatnts import *
from .gameobject import GameObject


class Apple(GameObject):
    """Class of game objectr appple"""

    def __init__(self, gameobjects, *args, **kwargs):
        super().__init__(gameobjects=gameobjects, color=APPLE_COLOR,
                         *args, **kwargs)
