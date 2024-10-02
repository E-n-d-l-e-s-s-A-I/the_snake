from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Abstract class of game object"""

    def __init__(self, position=(GRID_WIDTH / 2, GRID_HEIGHT / 2),
                 color=None):
        self.position = position
        self.body_color = color
        self.positions = [position]

    def draw(self):
        """Abstract method that draw game object"""
        pass

    @staticmethod
    def get_random_position():
        """Get random position"""
        return (randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1))

    def set_random_position(self, gameobjects):
        """Set random position without collisions"""
        position = self.get_random_position()
        while position in list(map(lambda x: x.positions, gameobjects)):
            position = self.get_random_position()

        self.position = position
        self.positions = position


class Apple(GameObject):
    """Class of game objectr appple"""

    def __init__(self):
        color = APPLE_COLOR
        super().__init__(color=color)
        self.randomize_position()

    def draw(self):
        """Draw method realisation of class Apple"""
        rect = pygame.Rect(tuple(GRID_SIZE * x for x in self.position),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Set apple random position in grid"""
        self.position = self.get_random_position()


class Snake(GameObject):
    """Class of game objectr snake"""

    def __init__(self):
        color = SNAKE_COLOR
        super().__init__(color=color)
        self.reset()

    def reset(self):
        """Reset snake to default"""
        self.length = 1
        self.current_lenght = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [self.position]

    @staticmethod
    def get_screen_positions(position):
        """Translate grid position to screen position"""
        return tuple(GRID_SIZE * x for x in position)

    def draw(self):
        """Draw method realisation of class Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(self.get_screen_positions(position),
                                (GRID_SIZE, GRID_SIZE)))

            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_screen_positions(self.positions[0]),
                                (GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.get_screen_positions(self.last),
                                    (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Update snake direction"""
        if self.next_direction:
            self.direction = self.next_direction
        self.next_direction = None

    def get_head_position(self):
        """Get position og snake head"""
        return self.positions[0]

    def move(self):
        """Move"""
        head_position = self.get_head_position()
        head_position = tuple(a + b for a, b in
                              zip(head_position, self.direction))
        head_position = self.round_position(head_position)
        if head_position in self.positions:
            self.reset()
            return True

        self.positions.insert(0, head_position)

        if self.current_lenght == self.length:
            self.last = self.positions.pop()
        else:
            self.length += 1

    @staticmethod
    def round_position(positon):
        """Round snake position"""
        return (abs(positon[0] % GRID_WIDTH),
                abs(positon[1] % GRID_HEIGHT))


def handle_keys(game_object):
    """Buttons click processing"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_UP and game_object.direction != DOWN):
                game_object.next_direction = UP

            elif (event.key == pygame.K_DOWN
                    and game_object.direction != UP):
                game_object.next_direction = DOWN

            elif (event.key == pygame.K_LEFT
                    and game_object.direction != RIGHT):
                game_object.next_direction = LEFT

            elif (event.key == pygame.K_RIGHT
                    and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Main method of programm"""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    snake.draw()
    apple.draw()
    pygame.display.update()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        is_crash = snake.move()

        if is_crash:
            # apple.set_random_position([snake])
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw()
            apple.draw()
            pygame.display.update()
            continue
        if snake.get_head_position() == apple.position:
            snake.current_lenght += 1
            apple.set_random_position([snake])

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
