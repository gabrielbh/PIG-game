import math

from AbstractPlayer import AbstractPlayer

"""
This player keeps track of it scoring turn (i.e, turns that have increased
a player score) and has a constant scoring turns parameter.
With these values calculates its hold value.
"""


class TScoringPlayer(AbstractPlayer):
    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        super(TScoringPlayer, self).__init__(index, name, goal_score,
                                             max_dice_value)
        self.t_score = 0
        self.current_player_score = 0
        self.hold_at_T = 0
        self.scoring_turns_parameter = 4

    def play(self, game_state, turn_score):
        # Check if we are starting a new game, if so - reset variables
        if self.new_game:
            self.reset_stat()
            self.new_game = False
        if turn_score == 0:
            # update t_score according to the last turn of the player
            if self.current_player_score != game_state[self.index]:
                self.t_score += 1
                self.current_player_score = game_state[self.index]
            self.hold_at_T = self.hold_at_t(game_state[self.index],
                                            self.t_score)
        if turn_score < self.hold_at_T:
            return True
        return False

    """
    This function finds the hold value for the current game stats.
    """
    def hold_at_t(self, score, t_score):
        return math.floor((100 - score) / (self.scoring_turns_parameter -
                                           t_score))
    """
    This function reset the value of the player variables when a new game
    is about to start.
    """
    def reset_stat(self):
        self.t_score = 0
        self.current_player_score = 0
        self.hold_at_T = 0
