from AbstractPlayer import AbstractPlayer

"""
This player is a human player which let the user act and choose manually rather
to roll the dice or end turn.
"""


class HumanPlayer(AbstractPlayer):
    def play(self, game_state, turn_score):
        while True:
            ans = input("Do you want to throw the dice? (y/n)")
            if ans == "y":
                return True
            elif ans == "n":
                return False
            print("This input is not valid, pleas answer in y/n")

