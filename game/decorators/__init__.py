"""package with decorators"""

from . import *
from functools import wraps


def singleton(cls):
    """Decorator for singelton classes"""
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


def collision_handler(other_cls):
    """Decorator for collisions handlers"""
    other_cls_name = other_cls.__name__.lower()

    def decorator(func):
        @wraps(func)
        def wrapper(self, other, game):
            return func(self, other, game)
        wrapper.__name__ = f'solve_collision_with_{other_cls_name}'
        return wrapper
    return decorator


def collision_with_yourself_handler(func):
    """Decorator for collisions handlers"""

    @wraps(func)
    def wrapper(self, other, game):
        return func(self, other, game)
    wrapper.__name__ = 'solve_collision_with_yourself'
    return wrapper