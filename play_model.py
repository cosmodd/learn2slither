from argparse import ArgumentParser

import pygame

from Game import Game, MoveOutcome, GameStates
from Renderer import Renderer
from qlearning import QLearningAgent

def main():
    parser = ArgumentParser(
        prog=__file__,
        description="Look a pre-trained model play",
    )

    parser.add_argument("model_path", type=str, help="Path to the model")
    arguments = parser.parse_args()

    # Setup pygame
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    agent = QLearningAgent.load_model(arguments.model_path)
    game = Game()
    renderer = Renderer(game)

    renderer.render(game)
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
            outcome = game.relative_move(action)

            if outcome == MoveOutcome.DIED:
                game.state = GameStates.GAME_OVER
                print(f"Game over!")
                continue

            renderer.render(game)
            pygame.display.flip()

        clock.tick(10)


if __name__ == "__main__":
    main()