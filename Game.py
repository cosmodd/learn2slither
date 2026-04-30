import random
from enum import Enum, auto


def _add_vec(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]

class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameStates(Enum):
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self, width=10, height=10, snake_length=3, green_apple_count=2, red_apple_count=1):
        self.state = GameStates.PLAYING
        self.size = (width, height)
        self.snake = []
        self.green_apples = []
        self.red_apples = []

        snake_initialized = False
        while not snake_initialized:
            try:
                self._init_snake(snake_length)
                snake_initialized = True
            except:
                pass

        self.spawn_green_apples(green_apple_count)
        self.spawn_red_apples(red_apple_count)

    def _in_bounds(self, position):
        (width, height) = self.size
        (x, y) = position
        return x > 0 and x < width and y > 0 and y < height

    def _is_space_occupied(self, position):
        return position in self.snake \
            or position in self.green_apples \
            or position in self.red_apples

    def _get_available_cells(self):
        (width, height) = self.size
        available_cells = []

        for y in range(height):
            for x in range(width):
                position = (x, y)
                if position in self.snake or position in self.green_apples or position in self.red_apples:
                    continue
                available_cells.append(position)

        return available_cells

    def _init_snake(self, length: int):
        (width, height) = self.size
        self.snake = [(
            random.randint(0, width - 1),
            random.randint(0, height - 1),
        )]

        for _ in range(length - 1):
            tail = self.snake[-1]
            directions = [
                _add_vec(tail, Directions.UP.value),
                _add_vec(tail, Directions.RIGHT.value),
                _add_vec(tail, Directions.DOWN.value),
                _add_vec(tail, Directions.LEFT.value),
            ]
            valid_directions = [*filter(lambda d: not self._is_space_occupied(d) and self._in_bounds(d), directions)]
            self.snake.append(random.choice(valid_directions))

    def spawn_green_apples(self, count: int = 1):
        available_cells = self._get_available_cells()

        for _ in range(count):
            index = random.randint(0, len(available_cells) - 1)
            self.green_apples.append(available_cells[index])
            available_cells.remove(available_cells[index])


    def spawn_red_apples(self, count: int = 1):
        available_cells = self._get_available_cells()

        for _ in range(count):
            index = random.randint(0, len(available_cells) - 1)
            self.red_apples.append(available_cells[index])
            available_cells.remove(available_cells[index])

    def move(self, direction: Directions):
        (width, height) = self.size
        next_head_position = _add_vec(self.snake[0], direction.value)

        # Check if the snake is going out of bounds
        if next_head_position[0] < 0 or next_head_position[0] >= width:
            return False

        if next_head_position[1] < 0 or next_head_position[1] >= height:
            return False

        # Check if the snake is going to collide with itself
        if next_head_position in self.snake:
            return False

        # Handle growth of the snake
        self.snake.insert(0, next_head_position)
        if next_head_position in self.green_apples:
            self.green_apples.remove(next_head_position)
            self.spawn_green_apples()
        elif next_head_position in self.red_apples:
            self.red_apples.remove(next_head_position)
            self.snake = self.snake[:-2]
            self.spawn_red_apples()
        else:
            self.snake = self.snake[:-1]

        return True