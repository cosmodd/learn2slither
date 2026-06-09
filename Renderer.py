import pygame.display

from Game import Game


def vec_sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]

class Renderer:
    def __init__(self, game: Game):
        pygame.init()
        pygame.font.init()

        self.cell_size = 80
        self.spacing = 8
        self.border_radius = 8
        self.background_color = (28, 26, 34)
        self.cell_color = (65, 59, 73)
        self.green_apple_color = (44, 255, 76)
        self.red_apple_color = (255, 80, 80)
        self.snake_color = (90, 75, 255)
        self.font = pygame.font.Font("assets/Monocraft.otf", 20)
        self.panel_width = 400

        (width, height) = game.size
        board_width = width * self.cell_size + (width + 1) * self.spacing
        self.panel_x = board_width
        board_height = height * self.cell_size + (height + 1) * self.spacing
        panel_width = self.panel_width + self.spacing

        self.screen = pygame.display.set_mode((board_width + panel_width, board_height))

    def get_cell_screen_position(self, x, y):
        return (
            (x + 1) * self.spacing + x * self.cell_size,
            (y + 1) * self.spacing + y * self.cell_size,
        )

    def _draw_text(self, text, color, position):
        text_surface = self.font.render(text, False, color)
        self.screen.blit(text_surface, position)

    def _draw_panel(self, game: Game):
        (sw, sh) = self.screen.get_size()
        panel_position = (self.panel_x, self.spacing)
        (px, py) = panel_position

        pygame.draw.rect(self.screen, self.cell_color, (
            panel_position,
            (self.panel_width, sh - self.spacing * 2)
        ), border_radius=self.border_radius)

        self._draw_text(f"Length: {len(game.snake)}", (255, 255, 255), (px + self.spacing * 2, py + self.spacing * 2))

    def render(self, game: Game):
        (width, height) = game.size
        self.screen.fill(self.background_color)

        # Draw grid
        for y in range(height):
            for x in range(width):
                screen_position = self.get_cell_screen_position(x, y)
                pygame.draw.rect(self.screen, self.cell_color, (screen_position, (self.cell_size, self.cell_size)), border_radius=self.border_radius)

        for i, (x, y) in enumerate(game.snake):
            screen_position = self.get_cell_screen_position(x, y)
            (sx, sy) = screen_position

            rect = (screen_position, (self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, self.snake_color, rect, border_radius=self.border_radius)

            if i == 0:
                pygame.draw.circle(self.screen, (255, 255, 255), center=(sx + self.cell_size / 2, sy + self.cell_size / 2), radius=self.cell_size / 4)
                pygame.draw.circle(self.screen, (0, 0, 0), center=(sx + self.cell_size / 2, sy + self.cell_size / 2), radius=self.cell_size / 6)

            if i > 0:
                previous_segment_position = game.snake[i - 1]
                (dx, dy) = vec_sub(previous_segment_position, (x, y))
                pygame.draw.rect(self.screen, self.snake_color, (
                    (sx + (self.cell_size / 2) * dx, sy + (self.cell_size / 2) * dy),
                    (self.cell_size, self.cell_size)
                ))

        for (x, y) in game.green_apples:
            screen_position = self.get_cell_screen_position(x, y)
            rect = (screen_position, (self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, self.green_apple_color, rect, border_radius=self.border_radius)

        for (x, y) in game.red_apples:
            screen_position = self.get_cell_screen_position(x, y)
            rect = (screen_position, (self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, self.red_apple_color, rect, border_radius=self.border_radius)

        self._draw_panel(game)