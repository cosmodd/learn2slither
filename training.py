import math

from rich import box
from rich.console import Group
from rich.live import Live
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.table import Table

from Game import Game, MoveOutcome, GameStates
from qlearning import QLearningAgent

def median(lst: list):
    lst = sorted(lst)
    n = len(lst)

    if n < 2:
        return lst[0]

    if n % 2 == 0:
        low_mid = n // 2
        high_mid = low_mid + 1
        return (lst[low_mid] + lst[high_mid]) / 2

    return lst[n // 2]

def average(lst: list):
    return sum(lst) / len(lst)

def _make_table(buckets: list):
    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold cyan",
        border_style="dim white",
        pad_edge=False
    )

    table.add_column("Episodes", justify="center", style="dim cyan", min_width=24)
    table.add_column("Avg Reward", justify="right", min_width=12)
    table.add_column("Max Reward", justify="right", min_width=12)
    table.add_column("Avg Length", justify="right", min_width=12)
    table.add_column("Max Length", justify="right", min_width=12)
    table.add_column("Avg Steps", justify="right", min_width=12)
    table.add_column("Max Steps", justify="right", min_width=12)

    window = buckets[-10:]
    for bucket in window:
        table.add_row(
            f"{bucket['start']} -> {bucket['end']}",
            f"{bucket['reward']['average']:8.1f}",
            f"{bucket['reward']['max']:>9}",
            f"{bucket['length']['average']:8.2f}",
            f"{bucket['length']['max']:>9}",
            f"{bucket['steps']['average']:8.1f}",
            f"{bucket['steps']['max']:>9}",
        )

    return table

def get_reward(outcome: MoveOutcome) -> float:
    reward_map = {
        MoveOutcome.DIED: -100,
        MoveOutcome.SHRUNK: -20,
        MoveOutcome.MOVED: -1,
        MoveOutcome.GREW: 20,
    }

    return reward_map[outcome]

def train_model(agent: QLearningAgent, num_episodes: int, bucket_count: int = 50):
    progress = Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TextColumn("[yellow]ε {task.fields[epsilon]:.4f}"),
        TextColumn("•"),
        TimeRemainingColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    )
    training_task = progress.add_task("Training model", total=num_episodes, epsilon=agent.epsilon)

    bucket_size = max(math.ceil(num_episodes / bucket_count), 100)
    bucket_count = math.ceil(num_episodes / bucket_size)
    snake_lengths = [[] for _ in range(bucket_count)]
    episodes_rewards = [[] for _ in range(bucket_count)]
    episodes_steps = [[] for _ in range(bucket_count)]
    completed_buckets = []

    def _make_display():
        return Group(progress, _make_table(completed_buckets))

    with Live(_make_display(), refresh_per_second=8) as live:
        for episode in range(num_episodes):
            game = Game()
            state = agent.get_state(game)
            episode_reward = 0
            max_snake_length = len(game.snake)
            steps = 1

            while game.state == GameStates.PLAYING:
                action = agent.choose_action(state, training=True)
                outcome = game.relative_move(action)

                reward = get_reward(outcome)
                episode_reward += reward

                if outcome == MoveOutcome.DIED:
                    agent.update_q(state, action, reward, None)
                    game.state = GameStates.GAME_OVER
                    break

                max_snake_length = max(max_snake_length, len(game.snake))
                next_state = agent.get_state(game)
                agent.update_q(state, action, reward, next_state)
                state = next_state
                steps += 1

            bucket_index = episode // bucket_size
            snake_lengths[bucket_index].append(max_snake_length)
            episodes_rewards[bucket_index].append(episode_reward)
            episodes_steps[bucket_index].append(steps)

            if (episode + 1) % bucket_size == 0:
                completed_buckets.append({
                    "start": bucket_index * bucket_size,
                    "end": (bucket_index + 1) * bucket_size,
                    "reward": {
                        "average": average(episodes_rewards[bucket_index]),
                        "max": max(episodes_rewards[bucket_index]),
                    },
                    "length": {
                        "average": average(snake_lengths[bucket_index]),
                        "max": max(snake_lengths[bucket_index]),
                    },
                    "steps": {
                        "average": average(snake_lengths[bucket_index]),
                        "max": max(episodes_steps[bucket_index]),
                    }
                })
                live.update(_make_display())

            agent.decay_epsilon(episode)
            progress.update(training_task, advance=1, epsilon=agent.epsilon)