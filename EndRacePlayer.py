from AbstractPlayer import AbstractPlayer

"""
This player choose to roll the dice in two cases:
a. If either player's score is e points or less from the goal.
b. If the turn score is less than the hold value
"""


class EndRacePlayer(AbstractPlayer):
    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        super(EndRacePlayer, self).__init__(index, name, goal_score,
                                            max_dice_value)
        # These are the optimal values we found for this policy
        self.c_val = 22
        self.e_val = 29
        self.d_val = 8

    def play(self, game_state, turn_score):
        # find opponent best score
        best_score = 0
        for val in game_state.values():
            if best_score < val != game_state[self.index]:
                best_score = val
        # calculate the hold value - k < c + ((j - i) / d)
        hold_val = self.c_val + round((best_score - game_state[self.index])
                                      / self.d_val)
        # check if either player score is e points or less from 100
        # or turn score is less than the hold value
        # and the player score + the turn score is less than the goal score
        if ((game_state[self.index] >= 100 - self.e_val or best_score >=
                100 - self.e_val) or turn_score < hold_val)\
                and game_state[self.index] + turn_score < self.goal_score:
            return True
        return False
