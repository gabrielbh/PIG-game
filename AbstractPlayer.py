"""
This is an abstract agent class
All the players are inherit from this class.
"""


class AbstractPlayer:
    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        self.index = index
        self.score = 0
        self.num_of_throws = 0
        self.goal_score = goal_score
        self.max_dice_value = max_dice_value
        self.name = name
        self.wins = 0
        self.new_game = False

    """
    This function return the index of the player object
    """
    def get_index(self):
        return self.index

    """
    This function returns the score of the player object
    """
    def get_score(self):
        return self.score

    """
    This function returns the number of dices the player thrown in the current
    turn.
    """
    def get_num_of_throws(self):
        return self.num_of_throws

    """
    This function should be implemented by each player according to his
    heuristic
    """
    def play(self, game_state, turn_score):
        pass

    """
    This function return a string representative of the player name
    """
    def get_name(self):
        return self.name

    """
    This function returns the number of games the player had won until now
    """
    def get_wins(self):
        return self.wins

    """
    This function add 1 to the sum of the player wins
    """
    def add_win(self):
        self.wins += 1

    """
    This function change the indicator to True, this indicator tell us if
    we are starting a new game
    """
    def change_game_stat(self):
        self.new_game = True
