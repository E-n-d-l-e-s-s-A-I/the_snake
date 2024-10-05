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
        self._initialization()
        self._create_start_game_objects()
        self._set_default_options()

    def _initialization(self):
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                               0, 32)
        pygame.display.set_caption(TITLE)
        self._game_field = Field(GRID_WIDTH, GRID_HEIGHT, self._screen)
        self._user_snake = None
        self._time = 0

    def _create_start_game_objects(self):
        self._create_game_object(UserSnake)
        self._create_game_object(Snake)
        self._create_game_object(Snake)
        self._create_game_object(Snake)
        self._create_game_object(Snake)
        self._create_game_object(Apple)
        self._create_game_object(Apple)
        self._create_game_object(Apple)
        self._create_game_object(Apple)

    def _set_default_options(self):
        self._speed = SPEED

    def _create_game_object(self, gameobject_cls):
        """Create gameobject by class"""
        gameobject = self._game_field.add_gameobject(gameobject_cls)
        if gameobject_cls is UserSnake:
            self._user_snake = gameobject

    def delete_game_object(self, gameobject: GameObject):
        """Delete gameobject"""
        self._game_field.delete_gameobject(gameobject)
        if gameobject is self._user_snake:
            self._game_over()

    def _draw_frame(self):
        """Draw field frame"""
        self._game_field.draw()
        pygame.display.update()

    def _make_time_difficult_up(self):
        """Make difficult up"""
        self._time += 1
        if self._time % 10 == 0:
            self._create_game_object(Apple)

        if self._time % 50 == 0:
            # cls._speed += 1
            self._create_game_object(Snake)

        if self._time % 100 == 0:
            self._create_game_object(Rock)

    def _move_moveable(self):
        for moveable in filter(lambda x: isinstance(x, MoveableGameObject),
                               self._game_field.gameobjects):
            moveable.set_direction()
            try:
                moveable.move()
            except ColliseWithYourSelfException:
                self.delete_game_object(moveable)

    def _game_over(self):
        self._game_field.reset()
        self._create_start_game_objects()
        self._set_default_options()

    def _solve_collisions(self):
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
            self._handle_keys()
            self._clock.tick(self._speed)

            self._move_moveable()
            self._solve_collisions()

            self._make_time_difficult_up()
            self._draw_frame()

    def _handle_keys(self):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
