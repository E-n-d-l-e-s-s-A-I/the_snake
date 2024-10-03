from game.constatnts import *
from .gameobject import GameObject


class Rock(GameObject):
    """Class of game objectr rock"""

    def __init__(self, gamefield, *args, **kwargs):
        super().__init__(gamefield=gamefield, color=ROCK_COLOR,
                         *args, **kwargs)
