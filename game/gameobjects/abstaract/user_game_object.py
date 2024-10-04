from random import choice

from .moveable_game_object import MoveableGameObject
from .unique_game_object import UniqueGameObject
from game.constatnts import *
import pygame


class UserGameObject(UniqueGameObject, MoveableGameObject):
    """class of moveable gameobject"""

    def set_direction(self):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_UP and self._direction != DOWN):
                    self._direction = UP

                elif (event.key == pygame.K_DOWN
                        and self._direction != UP):
                    self._direction = DOWN

                elif (event.key == pygame.K_LEFT
                        and self._direction != RIGHT):
                    self._direction = LEFT

                elif (event.key == pygame.K_RIGHT
                        and self._direction != LEFT):
                    self._direction = RIGHT
