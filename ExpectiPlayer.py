from AbstractPlayer import AbstractPlayer

"""
This player implement the tactic - Hold at 20 points in each turn.
As the name implies, the player chooses to roll the dice as long as his
turn score is lower than 20 points.
"""


class ExpectiPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        if turn_score >= 20:
            return False
        return True
