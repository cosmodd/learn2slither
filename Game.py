from enum import Enum, auto


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

        self._init_snake()
        self._init_green_apples()
        self._init_red_apples()

    def _init_snake(self):
        pass

    def _init_green_apples(self):
        pass

    def _init_red_apples(self):
        pass