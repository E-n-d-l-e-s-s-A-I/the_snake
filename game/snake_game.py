import pygame
from .constatnts import *
from .gameobjects import (Apple, Snake, Field, MoveableGameObject,
                          GameObject, Rock, UserSnake)
from .decorators import singleton


@singleton
class SnakeGame:
    """Class of game"""

    # Suppose that the game is singleton
    # Therefore, decided make all attributes at the class level

    def __init__(self):
        self._initialization()
        self._create_start_game_objects()
        self._set_default_options()

    @classmethod
    def _initialization(cls):
        cls._clock = pygame.time.Clock()
        cls._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption(TITLE)
        cls._game_field = Field(GRID_WIDTH, GRID_HEIGHT, cls._screen)

    @classmethod
    def _create_start_game_objects(cls):
        cls._create_game_object(UserSnake)
        cls._create_game_object(Snake)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Apple)
        cls._create_game_object(Rock)

    @classmethod
    def _set_default_options(cls):
        cls._speed = SPEED

    @classmethod
    def _create_game_object(cls, gameobject_cls):
        """Create gameobject by class, uniqe if it need"""
        gameobject = cls._game_field.add_gameobject(gameobject_cls)
        if gameobject_cls is UserSnake:
            cls._user_snake = gameobject

    @classmethod
    def _delete_game_object(cls, gameobject: GameObject):
        """Delete gameobject"""
        cls._game_field.delete_gameobject(gameobject)

    @classmethod
    def _move_snake(cls):
        """Move snake"""
        try:
            cls._user_snake.move()
        except Exception:
            cls._delete_game_object(cls._user_snake)
            cls._create_game_object(Snake)

    @classmethod
    def _apple_collision(cls, apple):
        """Handling a collision with a apple"""
        cls._user_snake.current_lenght += 1
        cls._delete_game_object(apple)
        cls._create_game_object(Apple)
        cls.difficult_up()

    @classmethod
    def _rock_collision(cls, rock):
        """Handling a collision with a rock"""
        cls._game_over()

    @classmethod
    def _check_snake_collisions(cls):
        """Сheck all snake possible collisions"""
        head_pos = cls._user_snake.get_head_position()
        object_on_position = cls._game_field[head_pos[0]][head_pos[1]]

        match object_on_position:
            case Apple():
                cls._apple_collision(object_on_position)
            case Rock():
                cls._rock_collision(object_on_position)

    @classmethod
    def _draw_frame(cls):
        """Draw field frame"""
        cls._game_field.draw()
        pygame.display.update()

    @classmethod
    def difficult_up(cls):
        """Make difficult up"""
        cls._create_game_object(Rock)
        cls._create_game_object(Apple)
        cls._speed += 1

    @classmethod
    def _move_moveable(cls):
        for moveable in filter(lambda x: isinstance(x, MoveableGameObject),
                               cls._game_field.gameobjects):
            moveable.set_direction()
            moveable.move()

    @classmethod
    def _game_over(cls):
        cls._game_field.reset()
        cls._create_start_game_objects()
        cls._set_default_options()

    def play(self):
        """Main method of game"""
        pygame.init
        while True:
            self._handle_keys()
            self._clock.tick(self._speed)

            self._move_moveable()

            self._check_snake_collisions()
            self._draw_frame()

    @classmethod
    def _handle_keys(cls):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
