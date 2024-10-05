import pygame
from .constatnts import *
from .gameobjects import (Apple, Snake, Field, MoveableGameObject,
                          GameObject, Rock, UserSnake, CollisionException,
                          ColliseWithYourSelfException)
from .decorators import singleton


@singleton
class SnakeGame:
    """Class of game"""

    # Suppose that the game is singleton
    # Therefore, decided make all attributes at the class level

    def __init__(self):
        pygame.init
        self._initialization()
        self._create_start_game_objects()
        self._set_default_options()

    @classmethod
    def _initialization(cls):
        cls._clock = pygame.time.Clock()
        cls._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption(TITLE)
        cls._game_field = Field(GRID_WIDTH, GRID_HEIGHT, cls._screen)
        cls._user_snake = None
        cls._time = 0

    @classmethod
    def _create_start_game_objects(cls):
        cls._create_game_object(UserSnake)
        cls._create_game_object(Snake)
        cls._create_game_object(Snake)
        cls._create_game_object(Snake)
        cls._create_game_object(Snake)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)

    @classmethod
    def _set_default_options(cls):
        cls._speed = SPEED

    @classmethod
    def _create_game_object(cls, gameobject_cls):
        """Create gameobject by class"""
        gameobject = cls._game_field.add_gameobject(gameobject_cls)
        if gameobject_cls is UserSnake:
            cls._user_snake = gameobject

    @classmethod
    def delete_game_object(cls, gameobject: GameObject):
        """Delete gameobject"""
        cls._game_field.delete_gameobject(gameobject)
        if gameobject is cls._user_snake:
            cls._game_over()

    @classmethod
    def _draw_frame(cls):
        """Draw field frame"""
        cls._game_field.draw()
        pygame.display.update()

    @classmethod
    def _make_time_difficult_up(cls):
        """Make difficult up"""
        cls._time += 1
        if cls._time % 10 == 0:
            cls._create_game_object(Apple)

        if cls._time % 50 == 0:
            # cls._speed += 1
            cls._create_game_object(Snake)

        if cls._time % 100 == 0:
            cls._create_game_object(Rock)

    @classmethod
    def _move_moveable(cls):
        for moveable in filter(lambda x: isinstance(x, MoveableGameObject),
                               cls._game_field.gameobjects):
            moveable.set_direction()
            try:
                moveable.move()
            except ColliseWithYourSelfException:
                cls.delete_game_object(moveable)

    @classmethod
    def _game_over(cls):
        cls._game_field.reset()
        cls._create_start_game_objects()
        cls._set_default_options()

    @classmethod
    def _solve_collisions(cls):
        while True:
            try:
                cls._game_field.update_moveable()
                break
            except CollisionException as e:
                obj1 = e.game_obj1
                obj2 = e.game_obj2
                obj1.collide_with(obj2, cls)

    def play(self):
        """Main method of game"""
        while True:
            self._handle_keys()
            self._clock.tick(self._speed)

            self._move_moveable()
            self._solve_collisions()

            self._make_time_difficult_up()
            self._draw_frame()

    @classmethod
    def _handle_keys(cls):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
