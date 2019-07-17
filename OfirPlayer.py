from AbstractPlayer import AbstractPlayer

"""
This player is a simple player that choose to roll the dice as long as the
sum of his own score and his current score is lower than the goal score and
the number of rolls in the turn is lower than is lucky number - 6.
"""


class OfirPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        if game_state[self.index] + turn_score >= self.goal_score \
                or self.num_of_throws >= self.max_dice_value:
            self.num_of_throws = 0
            return False
        self.num_of_throws += 1
        return True
