from AbstractPlayer import AbstractPlayer

"""
This player determines his actions based on his, and other players scores.
His default tactic will be the "hold to 20" tactic.
In case our total score is under 80, and an opponent with a higher than 80
total score exist, we won't stop until our turn score will be higher than 30.
In case of a total score that is higher than 80, and a lead of at least 10
points, we will be satisfied with a turn score which is higher than 15.
"""


class HeuristicPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        opponent_score = max(game_state.values())
        my_score = game_state[self.index]
        if my_score + turn_score >= 100:
            return False

        my_lead = my_score - opponent_score

        if my_score < 80 and opponent_score >= 80:
            want_pool = 30
        elif my_score >= 80 and (my_lead > 0 and my_lead <= 10):
            want_pool = 15
        else:
            want_pool = 20

        return turn_score < want_pool
