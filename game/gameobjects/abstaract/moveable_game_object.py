from random import choice

from .gameobject import GameObject
import game.constatnts as constants
import pygame


class MoveableGameObject(GameObject):
    """Class of moveable gameobject"""

    __time_without_move = 0
    __distance_with_out_turn = 0
    _distane_to_turn = 1
    _time_to_move = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._direction = choice([constants.RIGHT, constants.LEFT,
                                  constants.UP, constants.DOWN])
        self.tail = []

    def _get_available_directions(self):
        available_directions = [constants.LEFT, constants.RIGHT,
                                constants.UP, constants.DOWN]
        match self._direction:
            case constants.LEFT:
                available_directions.remove(constants.RIGHT)
            case constants.RIGHT:
                available_directions.remove(constants.LEFT)
            case constants.UP:
                available_directions.remove(constants.DOWN)
            case constants.DOWN:
                available_directions.remove(constants.UP)
        return available_directions

    def set_direction(self):
        """Set direction of move"""
        available_directions = self._get_available_directions()

        if self.__distance_with_out_turn == self._distane_to_turn:
            self._direction = choice(available_directions)
            self.__distance_with_out_turn = 0

    def draw(self, screen):
        """Extend draw for moveable object"""
        super().draw(screen)
        self._clear_tail(screen)

    def clear(self, screen):
        """Extend clear for moveable"""
        super().clear(screen)
        self._clear_tail(screen)

    def _clear_tail(self, screen):
        for position in self.tail:
            last_rect = pygame.Rect(self._get_screen_position(position),
                                    (constants.GRID_SIZE, constants.GRID_SIZE))
            pygame.draw.rect(screen, constants.BOARD_BACKGROUND_COLOR,
                             last_rect)
        self.tail = []

    def _move(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _get_tail_positions(self):
        raise NotImplementedError("Subclasses should implement this!")

    def move(self):
        """Move"""
        self.__time_without_move += 1
        if self.__time_without_move == self._time_to_move:
            self._move()
            if self._collise_with_yourself_check():
                raise ColliseWithYourSelfException
            self.__distance_with_out_turn += 1
            self.__time_without_move = 0

    def _collise_with_yourself_check(self):
        if len(self.positions) != len(set(self.positions)):
            raise ColliseWithYourSelfException()


class ColliseWithYourSelfException(Exception):
    """Exception caused when a Moveable Gameobject collise with yourself"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
