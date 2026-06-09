from argparse import ArgumentParser

import pygame

from Game import Game, MoveOutcome, GameStates
from main import draw_game
from qlearning import QLearningAgent

def main():
    parser = ArgumentParser(
        prog=__file__,
        description="Look a pre-trained model play",
    )

    parser.add_argument("model_path", type=str, help="Path to the model")
    arguments = parser.parse_args()

    agent = QLearningAgent.load_model(arguments.model_path)
    game = Game()

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    running = True
    draw_game(game, screen)
    pygame.display.flip()

    while running:

        # Handle keystrokes and some events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # Handle playing the game
        if game.state == GameStates.PLAYING:
            state = agent.get_state(game)
            action = agent.choose_action(state, training=False)
            print(f"Action: {action}")
            outcome = game.relative_move(action)

            if outcome == MoveOutcome.DIED:
                game.state = GameStates.GAME_OVER
                print(f"Game over!")
                continue

            draw_game(game, screen)
            pygame.display.flip()

        clock.tick(10)


if __name__ == "__main__":
    main()