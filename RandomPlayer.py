from AbstractPlayer import AbstractPlayer
import random

"""
This player is a simple player that choose to roll the dice or end turn -
randomly.
"""


class RandomPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        return random.randint(0, 5)