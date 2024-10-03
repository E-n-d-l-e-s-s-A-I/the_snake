from game.constatnts import *
from .gameobject import GameObject


class Rock(GameObject):
    """Class of game objectr rock"""

    def __init__(self, gameobjects, *args, **kwargs):
        super().__init__(gameobjects=gameobjects, color=ROCK_COLOR,
                         *args, **kwargs)
