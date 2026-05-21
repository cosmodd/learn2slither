import random
from collections import defaultdict

from Game import RelativeDirections


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
        max_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay_factor
