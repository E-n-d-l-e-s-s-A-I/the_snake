
import pygame
from random import randint


from game.constatnts import *

COLLSION_WITH_YOURSELF_HANDLER_NAME = 'solve_collision_with_yourself'


def get_name_for_solve_collision_handler(cls):
    """Get name for solve collision handler"""
    cls_name = cls.__name__.lower()
    return f'solve_collision_with_{cls_name}'


def find_solve_collision_method_in_mro(obj1, obj2):
    """Find solve collision method in mro"""
    for cls in type(obj2).mro():
        handler_name = get_name_for_solve_collision_handler(cls)
        if hasattr(obj1, handler_name):
            return obj1.__getattribute__(handler_name)


def find_solve_collision_method(obj1, obj2):
    """Find solve collision method frp obj1 and obj2"""
    if (type(obj1) is type(obj2)
            and hasattr(obj1, COLLSION_WITH_YOURSELF_HANDLER_NAME)):
        return COLLSION_WITH_YOURSELF_HANDLER_NAME

    solve_collsion_obj1_to_obj2 = find_solve_collision_method_in_mro(obj1,
                                                                     obj2)

    solve_collsion_obj2_to_obj1 = find_solve_collision_method_in_mro(obj2,
                                                                     obj1)

    return solve_collsion_obj1_to_obj2 or solve_collsion_obj2_to_obj1


class GameObject:
    """Abstract class of game object"""

    def collide_with(self, other, game):
        """Solve collision with seld and other object"""
        handler = find_solve_collision_method(self, other)

        if handler:
            handler(other, game)
        else:
            raise Exception('No specific collision handler for'
                            f'{type(self).__name__}with '
                            f'{type(other).__name__}')

    def __init__(self, *, gameobjects=[]):
        self._set_random_position(gameobjects)

    def draw(self, screen):
        """Draw game object on screen"""
        for position in self.positions:
            rect = (pygame.Rect(self._get_screen_position(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, self._color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def clear(self, screen):
        """Clear gameobject from screen"""
        for position in self.positions:
            rect = (pygame.Rect(self._get_screen_position(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def _set_random_position(self, gameobjects):
        """Set random position without collisions with gameobjects"""
        position = self._get_random_position()
        while position in list(map(lambda x: x.positions, gameobjects)):
            position = self._get_random_position()

        self.positions = [position]

    @staticmethod
    def _get_random_position():
        """Get random position"""
        return (randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1))

    @staticmethod
    def _round_position(positon):
        """Round snake position"""
        return (abs(positon[0] % GRID_WIDTH),
                abs(positon[1] % GRID_HEIGHT))

    @staticmethod
    def _get_screen_position(position):
        """Translate grid position to screen position"""
        return tuple(GRID_SIZE * x for x in position)

    def __str__(self):
        """Str implementation"""
        return f'{self.__class__.__name__} in {self.positions}'
