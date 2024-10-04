from game.constatnts import *
from .abstaract import StaticGameObject


class Rock(StaticGameObject):
    """Class of game objectr rock"""

    _color = ROCK_COLOR

    def __init__(self, gameobjects, *args, **kwargs):
        super().__init__(gameobjects=gameobjects, *args, **kwargs)
