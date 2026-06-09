import pygame

from Game import Game, Directions, GameStates, MoveOutcome
from Renderer import Renderer


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
    # Setup pygame
    pygame.init()
    pygame.key.set_repeat(100, 100)
    clock = pygame.time.Clock()
    running = True

    game = Game()
    renderer = Renderer(game)

    while running and game.state == GameStates.PLAYING:

        # Handle keystrokes and some events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

                move_outcome = None
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    move_outcome = game.move(Directions.UP)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move_outcome = game.move(Directions.DOWN)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move_outcome = game.move(Directions.RIGHT)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move_outcome = game.move(Directions.LEFT)

                if move_outcome == MoveOutcome.DIED:
                    print("YOU DIED.............")
                    game.state = GameStates.GAME_OVER

        renderer.render(game)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()