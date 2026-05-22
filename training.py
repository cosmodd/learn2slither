from argparse import ArgumentParser

from Game import Game, MoveOutcome, GameStates
from qlearning import QLearningAgent

def get_reward(outcome: MoveOutcome) -> float:
    reward_map = {
        MoveOutcome.DIED: -10,
        MoveOutcome.SHRUNK: -1,
        MoveOutcome.MOVED: -0.1,
        MoveOutcome.GREW: 1,
    }

    return reward_map[outcome]

def main():
    parser = ArgumentParser(
        prog=__file__,
        description="Train a Q-Learning agent on a Snake",
    )

    parser.add_argument("--episodes", type=int, default=100, help="Number of episodes to play")

    arguments = parser.parse_args()

    agent = QLearningAgent(
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=1.0,
        epsilon_decay_factor=0.995,
    )

    for episode in range(arguments.episodes):
        game = Game()
        state = agent.get_state(game.get_snake_vision())
        episode_reward = 0
        max_snake_length = len(game.snake)
        steps = 0

        print("Starting new game, starting states:")
        print(f"STATE: {state} | SNAKE_DIR: {game.last_direction}")

        while game.state == GameStates.PLAYING:
            action = agent.choose_action(state, training=True)
            outcome = game.relative_move(action)

            reward = get_reward(outcome)
            episode_reward += reward
            print(f"STATE: {state} | ACT: {action} | SNAKE_DIR: {game.last_direction} | OUTCOME: {outcome} | REWARD: {reward} | EP_REWARD: {episode_reward}")

            if outcome == MoveOutcome.DIED:
                agent.update_q(state, action, reward, None)
                game.state = GameStates.GAME_OVER
                break

            max_snake_length = max(max_snake_length, len(game.snake))
            next_state = agent.get_state(game.get_snake_vision())
            agent.update_q(state, action, reward, next_state)
            state = next_state
            steps += 1

        agent.decay_epsilon()
        print(f"Episode: {episode + 1} | Reward: {episode_reward} | Epsilon: {agent.epsilon} | Max Snake Length: {max_snake_length} | Steps: {steps}")

if __name__ == "__main__":
    main()