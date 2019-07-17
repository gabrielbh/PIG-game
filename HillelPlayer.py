import random
from AbstractPlayer import AbstractPlayer

"""
This player continue to roll the dice in each turn until the sum of his current
turn score and his own score is higher than his opponent score.
"""


class HillelPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        if not random.randint(0, 10):
            return False

        if game_state[self.index] + turn_score >= self.goal_score:
            return False

        for score in game_state.values():
            if score > game_state[self.index] + turn_score:
                return True
        return False
