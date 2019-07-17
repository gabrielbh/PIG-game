from AbstractPlayer import AbstractPlayer

"""
This player throws until the turn score is larger than 19, and after he
threw at least five times.
"""


class GoobiPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        if game_state[self.index] + turn_score >= self.goal_score:
            return False
        return turn_score < (self.max_dice_value - 2) * 5\
            and self.num_of_throws < self.max_dice_value - 1
