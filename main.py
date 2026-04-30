import pygame

from Game import Game, Directions

def print_game(game: Game):
    (width, height) = game.size

    for y in range(height + 2):
        for x in range(width + 2):
            char = '  '

            if x < 1 or y < 1 or x > width or y > height:
                # char = '██'
                char = '🧱'

            game_pos = (x - 1, y - 1)

            if game_pos in game.snake:
                char = '🟢'
            if game_pos == game.snake[0]:
                char = '🤢'

            if game_pos in game.green_apples:
                char = '🍏'

            if game_pos in game.red_apples:
                char = '🍎'

            print(char, end='')
        print()

def main():
    game = Game()

    # Setup pygame
    pygame.init()
    pygame.key.set_repeat(100, 100)
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    running = True

    (width, height) = game.size
    cell_size = pygame.display.get_surface().get_size()[0] / width

    while running:

        # Handle keystrokes and some events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    game.move(Directions.UP)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    game.move(Directions.DOWN)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    game.move(Directions.RIGHT)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    game.move(Directions.LEFT)


        screen.fill((214, 30, 73))

        # Draw grid
        for y in range(height):
            for x in range(width):
                screen_position = (x * cell_size, y * cell_size)
                pygame.draw.rect(screen, (163, 16, 51), (screen_position, (cell_size, cell_size)), 1)

        snake_colors = [
            (65, 68, 250),
            (40, 42, 173),
            (28, 29, 120),
        ]
        for i, (x, y) in enumerate(game.snake):
            screen_position = (x * cell_size, y * cell_size)
            rect = (screen_position, (cell_size, cell_size))
            if i == 0:
                pygame.draw.rect(screen, snake_colors[0], rect)
            else:
                pygame.draw.rect(screen, snake_colors[1 + i % 2], rect)

        for (x, y) in game.green_apples:
            screen_position = (x * cell_size, y * cell_size)
            rect = (screen_position, (cell_size, cell_size))
            pygame.draw.rect(screen, (68, 250, 65), rect)

        for (x, y) in game.red_apples:
            screen_position = (x * cell_size, y * cell_size)
            rect = (screen_position, (cell_size, cell_size))
            pygame.draw.rect(screen, (250, 65, 65), rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()