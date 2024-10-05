import pygame
from .constatnts import *
from .gameobjects import (Apple, Snake, Field, MoveableGameObject,
                          GameObject, Rock, UserSnake, CollisionException,
                          ColliseWithYourSelfException)


class SnakeGame:
    """Class of game"""

    # Suppose that the game is singleton
    # Therefore, decided make all attributes at the class level

    def __init__(self):
        pygame.init
        self.__initialization()
        self._create_start_game_objects()
        self._set_default_options()

    def __initialization(self):
        """Initialization method"""
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                               0, 32)
        pygame.display.set_caption(TITLE)
        self._game_field = Field(GRID_WIDTH, GRID_HEIGHT, self._screen)
        self._user_snake = None
        self._time = 0

    def _create_start_game_objects(self):
        """Create start game objects, can be implemented in subclasses"""
        self._create_game_object(UserSnake)
        self._create_game_object(Apple)

    def _set_default_options(self):
        """Set default options, can be implemented in subclasses"""
        self._speed = SPEED

    def _create_game_object(self, gameobject_cls):
        """Create gameobject by class"""
        gameobject = self._game_field.add_gameobject(gameobject_cls)
        if gameobject_cls is UserSnake:
            self._user_snake = gameobject

    def _delete_game_object(self, gameobject: GameObject):
        """Delete gameobject"""
        self._game_field.delete_gameobject(gameobject)
        if gameobject is self._user_snake:
            self.__game_over()

    def __draw_frame(self):
        """Draw field frame"""
        self._game_field.draw()
        pygame.display.update()

    def _make_time_difficult_up(self):
        """Make difficult up, can be implemented in subclasses"""
        if self._time % 50 == 0:
            self._speed += 1

    def __move_moveable(self):
        """Move all moveable objects in field"""
        for moveable in filter(lambda x: isinstance(x, MoveableGameObject),
                               self._game_field.gameobjects):
            moveable.set_direction()
            try:
                moveable.move()
            except ColliseWithYourSelfException:
                self._delete_game_object(moveable)

    def __game_over(self):
        """Game over method"""
        self._game_field.reset()
        self._create_start_game_objects()
        self._set_default_options()

    def __solve_collisions(self):
        """Solve all collisions, it calls before __move_all_moveable"""
        while True:
            try:
                self._game_field.update_moveable()
                break
            except CollisionException as e:
                obj1 = e.game_obj1
                obj2 = e.game_obj2
                obj1.collide_with(obj2, self)

    def play(self):
        """Main method of game"""
        while True:
            self.__handle_keys()
            self._clock.tick(self._speed)

            self.__move_moveable()
            self.__solve_collisions()

            self._time += 1
            self._make_time_difficult_up()

            self.__draw_frame()

    def __handle_keys(self):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
