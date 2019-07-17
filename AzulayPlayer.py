import random
from AbstractPlayer import AbstractPlayer

"""
This player is a simple player that throws until he wins. (does not hold)
"""


class AzulayPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        if not random.randint(0, 10):
            return False
        return game_state[self.index] + turn_score < self.goal_score
