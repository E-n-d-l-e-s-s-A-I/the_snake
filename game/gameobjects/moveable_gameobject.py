from random import choice
import pygame

from .gameobject import GameObject
from game.constatnts import *


class MoveableGameobject(GameObject):
    """class of moveable gameobject"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None

    def update_direction(self):
        """Update moveable gameobject direction"""
        if self.next_direction:
            self.direction = self.next_direction
        self.next_direction = None
