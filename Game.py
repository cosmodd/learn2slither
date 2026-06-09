import random
from enum import Enum, auto


def _add_vec(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class RelativeDirections(Enum):
    LEFT = auto()
    STRAIGHT = auto()
    RIGHT = auto()

class GameStates(Enum):
    PLAYING = auto()
    GAME_OVER = auto()

class MoveOutcome(Enum):
    GREW = auto()
    SHRUNK = auto()
    MOVED = auto()
    DIED = auto()

class Game:
    def __init__(
        self,
        width= 10,
        height= 10,
        snake_length= 3,
        green_apple_count= 2,
        red_apple_count= 1,
    ):
        self.state = GameStates.PLAYING
        self.size = (width, height)
        self.snake = []
        self.last_direction = None
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
        return 0 <= x < width and 0 <= y < height

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

        opposites = {
            Directions.UP: Directions.DOWN,
            Directions.DOWN: Directions.UP,
            Directions.LEFT: Directions.RIGHT,
            Directions.RIGHT: Directions.LEFT,
        }

        for index in range(length - 1):
            tail = self.snake[-1]
            directions = [
                (Directions.UP, _add_vec(tail, Directions.UP.value)),
                (Directions.RIGHT, _add_vec(tail, Directions.RIGHT.value)),
                (Directions.DOWN, _add_vec(tail, Directions.DOWN.value)),
                (Directions.LEFT, _add_vec(tail, Directions.LEFT.value)),
            ]
            valid_directions = [*filter(lambda d: not self._is_space_occupied(d[1]) and self._in_bounds(d[1]), directions)]
            random_direction = random.choice(valid_directions)
            if index == 0:
                self.last_direction = opposites[random_direction[0]]
            self.snake.append(random_direction[1])

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

    def _handle_snake_next_position(self, next_head_position) -> MoveOutcome:
        if not self._in_bounds(next_head_position):
            return MoveOutcome.DIED

        if next_head_position in self.snake and next_head_position != self.snake[-1]:
            return MoveOutcome.DIED

        self.snake.insert(0, next_head_position)
        if next_head_position in self.green_apples:
            self.green_apples.remove(next_head_position)
            self.spawn_green_apples()
            return MoveOutcome.GREW

        if next_head_position in self.red_apples:
            self.red_apples.remove(next_head_position)
            self.snake = self.snake[:-2]
            self.spawn_red_apples()
            if len(self.snake) > 0:
                return MoveOutcome.SHRUNK
            else:
                return MoveOutcome.DIED

        self.snake = self.snake[:-1]
        return MoveOutcome.MOVED

    def move(self, direction: Directions) -> MoveOutcome:
        next_head_position = _add_vec(self.snake[0], direction.value)
        outcome = self._handle_snake_next_position(next_head_position)

        if outcome != MoveOutcome.DIED:
            self.last_direction = direction

        return outcome

    def relative_move(self, relative_direction: RelativeDirections):
        left_mapping = {
            Directions.UP: Directions.LEFT,
            Directions.RIGHT: Directions.UP,
            Directions.DOWN: Directions.RIGHT,
            Directions.LEFT: Directions.DOWN,
        }

        right_mapping = {
            Directions.UP: Directions.RIGHT,
            Directions.RIGHT: Directions.DOWN,
            Directions.DOWN: Directions.LEFT,
            Directions.LEFT: Directions.UP,
        }

        direction = self.last_direction

        if relative_direction == RelativeDirections.LEFT:
            direction = left_mapping[self.last_direction]

        if relative_direction == RelativeDirections.RIGHT:
            direction = right_mapping[self.last_direction]

        outcome = self._handle_snake_next_position(_add_vec(self.snake[0], direction.value))

        if outcome != MoveOutcome.DIED:
            self.last_direction = direction

        return outcome

    def _get_cell_character(self, position):
        if not self._in_bounds(position):
            return "W"

        if position == self.snake[0]:
            return "H"
        elif position in self.snake:
            return "S"

        if position in self.green_apples:
            return "G"

        if position in self.red_apples:
            return "R"

        return "0"

    def get_snake_vision(self):
        (width, height) = self.size
        (x, y) = self.snake[0]

        vision = ["", "", "", ""]

        # Handle UP vision
        for i in reversed(range(y)):
            vision[0] += self._get_cell_character((x, i))
        vision[0] += "W"

        # Handle RIGHT vision
        for i in range(x + 1, width):
            vision[1] += self._get_cell_character((i, y))
        vision[1] += "W"

        # Handle DOWN vision
        for i in range(y + 1, height):
            vision[2] += self._get_cell_character((x, i))
        vision[2] += "W"

        # Handle LEFT vision
        for i in reversed(range(x)):
            vision[3] += self._get_cell_character((i, y))
        vision[3] += "W"

        return tuple(vision)

    def get_relative_snake_vision(self):
        absolute_vision = self.get_snake_vision()
        relative_snake_vision = []

        dir_to_index = {
            Directions.UP: 0,
            Directions.RIGHT: 1,
            Directions.DOWN: 2,
            Directions.LEFT: 3,
        }

        last_direction_index = dir_to_index[self.last_direction]
        left_index = (last_direction_index + 4 - 1) % 4
        right_index = (last_direction_index + 4 + 1) % 4

        relative_snake_vision.append(absolute_vision[left_index])
        relative_snake_vision.append(absolute_vision[last_direction_index])
        relative_snake_vision.append(absolute_vision[right_index])
        return relative_snake_vision