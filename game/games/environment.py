from game.snake_game import SnakeGame
from game.gameobjects import UserSnake, Apple, Snake, Rock


class Environment(SnakeGame):
    """Class of classic snake game"""

    def _create_start_game_objects(self):
        """Implementation of create_start_game_objects()"""
        self._create_game_object(Apple)
        self._create_game_object(Apple)
        self._create_game_object(Apple)

        self._create_game_object(Snake)
        self._create_game_object(Snake)
        self._create_game_object(Snake)

    def _make_time_difficult_up(self):
        """Implementation of make difficult up"""
        if self._time % 10 == 0:
            self._create_game_object(Apple)
        if self._time % 50 == 0:
            self._speed += 1
            self._create_game_object(Snake)
        if self._time % 100 == 0:
            self._create_game_object(Rock)
