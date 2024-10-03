import pygame

from .constatnts import *
from .gameobjects import (Apple, Snake, Field, MoveableGameobject, GameObject,
                          SnakeEatYourselfException, Rock)

class SnakeGame:
    """class of game"""

    def __init__(self):
        # Pygame init
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption(TITLE)

        # Gameobjects init
        self._game_field = Field(GRID_WIDTH, GRID_HEIGHT, self.screen)
        self._create_start_game_objects()

        # Game options init
        self._set_default_options()

    def _create_start_game_objects(self):
        self._create_game_object(Snake)
        self._create_game_object(Apple)
        self._create_game_object(Apple)
        self._create_game_object(Rock)

    def _set_default_options(self):
        self.speed = SPEED

    @property
    def _snake(self):
        """Snake prporty"""
        # It's not optimized
        # But it's beauty
        # Beautiful is better than ugly. - Zen of Pthon
        return filter(lambda x: isinstance(x, Snake),
                      self._game_field.gameobjects).__next__()

    @property
    def _apples(self):
        """Apple prporty"""
        return list(filter(lambda x: isinstance(x, Apple),
                    self._game_field.gameobjects))

    def _create_game_object(self, cls: GameObject):
        """Create game object by class, uniqe if it need"""
        cls(gamefield=self._game_field)

    def _move_moveable_gameobjects(self):
        """Call _handle_keys() for MoveableGameobject objects"""
        for gameobject in self._game_field.gameobjects:
            if isinstance(gameobject, MoveableGameobject):
                self._handle_keys(gameobject)
                gameobject.update_direction()

    def _move_snake(self):
        """Move snake"""
        try:
            self._snake.move()
        except SnakeEatYourselfException:
            self._snake.delete()
            self._create_game_object(Snake)

    def _apple_collision(self, apple):
        """Handling a collision with a apple"""
        self._snake.current_lenght += 1
        apple.delete()
        self._create_game_object(Apple)
        self.difficult_up()

    def _rock_collision(self, rock):
        """Handling a collision with a rock"""
        self._game_over()

    def _check_snake_collisions(self):
        """Сheck all snake possible collisions"""
        head_pos = self._snake.get_head_position()
        object_on_position = self._game_field[head_pos[0]][head_pos[1]]

        match object_on_position:
            case Apple():
                self._apple_collision(object_on_position)
            case Rock():
                self._rock_collision(object_on_position)

    def play(self):
        """Main method of game"""
        pygame.init
        while True:
            self.clock.tick(self.speed)

            self._move_moveable_gameobjects()
            self._move_snake()
            self._check_snake_collisions()
            self._draw_frame()

    def _draw_frame(self):
        """Draw field frame"""
        self._game_field.draw()
        pygame.display.update()

    def difficult_up(self):
        """Make dissicult ap"""
        self._create_game_object(Rock)
        self._create_game_object(Apple)
        self.speed += 1

    def _game_over(self):
        self._game_field.reset()
        self._create_start_game_objects()
        self._set_default_options()

    @staticmethod
    def _handle_keys(gameobject):
        """Buttons click processing"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_UP and gameobject.direction != DOWN):
                    gameobject.next_direction = UP

                elif (event.key == pygame.K_DOWN
                        and gameobject.direction != UP):
                    gameobject.next_direction = DOWN

                elif (event.key == pygame.K_LEFT
                        and gameobject.direction != RIGHT):
                    gameobject.next_direction = LEFT

                elif (event.key == pygame.K_RIGHT
                        and gameobject.direction != LEFT):
                    gameobject.next_direction = RIGHT
