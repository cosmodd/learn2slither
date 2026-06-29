from argparse import ArgumentParser

import pygame

import training
from Game import Game, GameStates, Directions, MoveOutcome
from Renderer import Renderer
from qlearning import QLearningAgent


def init_args_parser():
    parser = ArgumentParser(prog=__file__)
    subparsers = parser.add_subparsers(title="Commands", dest='command')

    play_parser = subparsers.add_parser('play', help='Play the game yourself')
    play_parser.add_argument("--speed", "-s", help="How fast will the game play", metavar="speed", type=int, default=8)
    play_parser.add_argument("--step-by-step", "-S", help="Step-by-step mode", action="store_true")

    train_parser = subparsers.add_parser("train", help="Train a model using Q-Learning")
    train_parser.add_argument("--save", "-s", help="Save the trained model", metavar="filepath", type=str)
    train_parser.add_argument("--visuals", "-v", help="Visualize training sessions", action="store_true")
    train_parser.add_argument("--episodes", "-e", help="Number of episodes to play", metavar="episodes", type=int, default=100)

    run_parser = subparsers.add_parser('run', help='Run a trained model')
    run_parser.add_argument("filepath", help="Filepath of the trained model", type=str)
    run_parser.add_argument("--speed", "-s", help="How fast will the game play", metavar="speed", type=int, default=15)
    run_parser.add_argument("--step-by-step", "-S", help="Step-by-step mode", action="store_true")

    return parser

def main():
    parser = init_args_parser()
    arguments = parser.parse_args()

    pygame.init()
    pygame.key.set_repeat(100, 100)
    clock = pygame.time.Clock()

    if arguments.command == "play":
        running = True
        game = Game()
        renderer = Renderer(game)
        renderer.render(game)
        pygame.display.flip()

        while running and game.state == GameStates.PLAYING:
            direction = game.last_direction

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type != pygame.KEYDOWN:
                    continue

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction = Directions.UP
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction = Directions.RIGHT
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    direction = Directions.DOWN
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction = Directions.LEFT

            if game.move(direction) == MoveOutcome.DIED:
                print("YOU DIED.....................")
                game.state = GameStates.GAME_OVER

            renderer.render(game)
            pygame.display.flip()
            clock.tick(arguments.speed)

    elif arguments.command == "train":
        number_of_episodes = arguments.episodes
        agent = QLearningAgent(
            learning_rate=0.1,
            discount_factor=0.99,
            epsilon=1,
            epsilon_decay_factor=(0.02 ** (1 / number_of_episodes)),
        )
        training.train_model(agent, number_of_episodes)

        if arguments.save:
            agent.save_model(arguments.save)
            print(f"Saved model to {arguments.save}")

    elif arguments.command == "run":
        running = True

        agent = QLearningAgent.load_model(arguments.filepath)
        game = Game()
        renderer = Renderer(game)

        renderer.render(game)
        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

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

            clock.tick(arguments.speed)


if __name__ == "__main__":
    main()