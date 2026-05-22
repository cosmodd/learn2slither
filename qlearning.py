import os
import pickle
import random
from collections import defaultdict

from Game import RelativeDirections, Game


class QLearningAgent:
    def __init__(self,
                 learning_rate=0.1,
                 discount_factor=0.9,
                 epsilon=1.0,
                 epsilon_decay_factor=0.99):
        """
        Initialize a Q-Learning agent.
        :param learning_rate: how much to update the q-values
        :param discount_factor: how much to value future rewards
        :param epsilon: initial exploration rate
        """
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay_factor = epsilon_decay_factor

        self.actions = list(RelativeDirections)

    def get_state(self, game: Game):
        def get_char_distance(dir, char):
            for i, c in enumerate(dir):
                if c == char:
                    return i + 1
            return 0

        def encode_direction(direction):
            return (
                get_char_distance(direction, "G"),
                get_char_distance(direction, "R"),
                get_char_distance(direction, "S"),
                get_char_distance(direction, "W"),
            )

        return game.last_direction, tuple(encode_direction(d) for d in game.get_snake_vision())

    def choose_action(self, state, training=True):
        if training and random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            return max(self.actions, key=lambda i: self.q_table[state][i])

    def update_q(self, state, action, reward, next_state):
        """
        Q learning update: Q(state, action) += learning_rate * (reward + discount_factor * Q(next_state, a) - Q(state, action))
        """
        current_q = self.q_table[state][action]
        if next_state is None:
            max_next_q = 0
        else:
            max_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def decay_epsilon(self, episode: int = None):
        if episode is None:
            self.epsilon = max(0.01, self.epsilon * self.epsilon_decay_factor)
        else:
            self.epsilon = max(0.01, 1.0 * (self.epsilon_decay_factor ** episode))

    def save_model(self, filepath: str):
        q_table = {state: dict(actions) for state, actions in self.q_table.items()}

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        pickle.dump({
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "epsilon": self.epsilon,
            "q_table": q_table
        }, open(filepath, "wb"))

    @staticmethod
    def load_model(filepath: str):
        model = pickle.load(open(filepath, "rb"))
        agent = QLearningAgent()

        agent.learning_rate = model["learning_rate"]
        agent.discount_factor = model["discount_factor"]
        agent.epsilon = model["epsilon"]
        agent.q_table = defaultdict(lambda: defaultdict(float), {state: defaultdict(float, actions) for state, actions in model["q_table"].items()})

        return agent

