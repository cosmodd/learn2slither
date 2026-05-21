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
    number_of_games = 100
    agent = QLearningAgent()

    for episode in range(number_of_games):
        game = Game()
        state = agent.get_state(game.get_snake_vision())
        episode_reward = 0

        print("Starting new game, starting states:")
        print(f"STATE: {state} | SNAKE_DIR: {game.last_direction}")

        while game.state == GameStates.PLAYING:
            action = agent.choose_action(state, training=True)
            outcome = game.relative_move(action)

            reward = get_reward(outcome)
            episode_reward += reward
            print(f"STATE: {state} | ACT: {action} | SNAKE_DIR: {game.last_direction} | OUTCOME: {outcome} | REWARD: {reward} | EP_REWARD: {episode_reward}")

            if outcome == MoveOutcome.DIED:
                game.state = GameStates.GAME_OVER
                break

            next_state = agent.get_state(game.get_snake_vision())
            agent.update_q(state, action, reward, next_state)
            state = next_state

        agent.decay_epsilon()
        print(f"Episode: {episode + 1} | Reward: {episode_reward} | Epsilon: {agent.epsilon}")

if __name__ == "__main__":
    main()