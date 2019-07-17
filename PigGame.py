import random
from random import shuffle
import HumanPlayer
import RandomPlayer
import AzulayPlayer
import GoobiPlayer
import HillelPlayer
import OfirPlayer
import HeuristicPlayer
import learningAgent
import ExpectiPlayer
import TScoringPlayer
import EndRacePlayer
import QLearningAgent
import ApproxQLearningAgent
import sys

APPROX_QLEARNING_STRING_REP = "Approx Q Player"
APPROX_QLEARNING_PLAYER_INDEX = '12'
QLEARNING_PLAYER_STRING_REP = "Q Player"
QLEARNING_PLAYER_INDEX = '11'
END_RACE_PLAYER_STRING_REP = "End Race Player"
END_RACE_PLAYER_INDEX = '10'
TSCORING_PLAYER_STRING_REP = "T Scoring Player"
TSCORING_PLAYER_INDEX = '9'
EXPECTI_PLAYER_STRING_REP = "Expecti Player"
EXPECTI_PLAYER_INDEX = '8'
RANDOM_PLAYER_STRING_REP = "Random Player"
RANDOM_PLAYER_INDEX = '7'
HUMAN_PLAYER_STRING_REP = "Human Player"
HUMAN_PLAYER_INDEX = '6'
HILLEL_PLAYER_STRING_REP = "Hillel Player"
HILLEL_PLAYER_INDEX = '5'
OFIR_PLAYER_STRING_REP = "Ofir Player"
OFIR_PLAYER_INDEX = '4'
AZULAY_PLAYER_STRING_REP = "Azulay Player"
AZULAY_PLAYER_INDEX = '3'
HEURISTIC_PLAYER_STRING_REP = "Heuristic Player"
HEURISTIC_PLAYER_INDEX = '2'
LEARNING_PLAYER_INDEX = '1'
LEARNING_PLAYER_STRING_REP = "Learning Player"
GOOBI_PLAYER_INDEX = '0'
GOOBI_PLAYER_STRING_REP = "Goobi Player"
RESET_SCORE = 1
MIN_DICE_VALUE = 1
MAX_DICE_VALUE = 6
FIRST_PLAYER = 0
CONTINUE = 0
GAME_OVER = 1
GAME_OVER_MSG = "game over. winner is: "
GOOBI_PLAYER = 0
LEARNING_PLAYER = 1
HEURISTIC_PLAYER = 2
AZULAY_PLAYER = 3
OFIR_PLAYER = 4
HILLEL_PLAYER = 5
HUMAN_PLAYER = 6
RANDOM_PLAYER = 7
EXPECTI_PLAYER = 8


"""
This class defines a pig game representation.
By using this class we simulates a multiple games (as we desire) of pig game.
The object of the jeopardy dice game Pig is to be the first player to reach 100
points. Each player's turn consists of repeatedly rolling a die. After each
roll, the player is faced with two choices:
1)	roll again: . If the player rolls a 1, the player scores nothing and it
becomes the opponent's turn. . If the player rolls a number other than 1, the
 number is added to the player's turn total and the player's turn continues.
2)	Hold: . If the player holds (he decline to roll again), the turn total, the
sum of the rolls during the turn, is added to the player's score, and it
becomes the opponent's turn.
"""


class PigGame(object):
    """
    This is the constructor of the class.
    It receives a goal score and players types
    """
    def __init__(self, goal_score, players):
        print_mode = int(sys.argv[3])
        if print_mode:
            # Print welcome messages in the beginning of the game only if
            # the player input print bit is on
            print()
            print("**********Welcome To Pig - Dice Game**********")
            print()
            print("                         ,.")
            print("                        (_|,.")
            print("                       ,' /, )_______   _")
            print("                    __j o``-'        `.'-)'")
            print("                   (')                 \'")
            print("                    `-j                |")
            print("                      `-._(           /")
            print("                         |_\  |--^.  /")
            print("                        /_]'|_| /_)_/")
            print("                           /_]'  /_]'")
            print()
            print("*******************Good Luck******************")
            print()
        self.players = players
        self.max_score = goal_score
        self.current_player = players[FIRST_PLAYER]
        self.num_of_players = len(players)
        self.state = {}
        for i in range(self.num_of_players):
            self.state[players[i].get_index()] = 0
        if print_mode:
            print("The participating players are: ", end="")
            for index, player in enumerate(players):
                if index != len(players) - 1:
                    print(player.get_name() + ", ", end="")
                else:
                    print(player.get_name())
            print()

    """
    This is a simple function to simulates a dice.
    This function returns number between 1 to 6 with uniform distribution
    """
    @staticmethod
    def roll_dice():
        return random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE)

    """
    This function responsible for running a player turn.
    In each turn, the player is asked to roll the dice or end his turn.
    """
    def play_turn(self, player):
        print_mode = int(sys.argv[3])
        if print_mode:
            print("current player: ", player.get_name())
        current_turn_score = 0
        # ask the player what will be his next move - roll the dice or end turn
        while player.play(self.state, current_turn_score):
            current_roll = self.roll_dice()
            if print_mode:
                print(str(current_roll) + " rolled by " + player.get_name())
            if current_roll != RESET_SCORE:
                current_turn_score += current_roll
            else:
                current_turn_score = 0
                break
        # after the player end his turn, sum his turn score to his overall
        # score and check if he reached the goal score (100)
        self.state[player.get_index()] += current_turn_score
        if self.state[player.get_index()] >= self.max_score:
            player.add_win()
            for player in self.players:
                player.change_game_stat()
            if print_mode:
                print(GAME_OVER_MSG + player.get_name())
                print()
                print("Final score: ")
                for player in self.players:
                    print(player.get_name() + ": " + str(
                        self.state[player.get_index()]))
            return GAME_OVER
        return CONTINUE

    """
    This function responsible for running the game. As long as the game is not
    over, after each player turn it change the current player to the next
    player.
    """
    def run_game(self):
        print_mode = int(sys.argv[3])
        while self.play_turn(self.current_player) != GAME_OVER:
            self.current_player = self.players[
                (self.players.index(self.current_player) + 1) %
                self.num_of_players]
            if print_mode:
                print("Current score - {", end="")
                for index, player in enumerate(self.players):
                    if index != len(self.players) - 1:
                        print(player.get_name() + ": " + str(
                            self.state[player.get_index()]) + ", ", end="")
                    else:
                        print(player.get_name() + ": " + str(
                            self.state[player.get_index()]) + "}")
                        print()

        return max(self.state, key=self.state.get)


"""
This function creates the player objects according to the user input value.
"""


def get_players():
    players = []
    # get the user input which contains the players type values and
    # create the player objects accordingly.
    input_list = sys.argv[1].split(',')
    for index, player in enumerate(input_list):
        if player == GOOBI_PLAYER_INDEX:
            goobi_player = GoobiPlayer.GoobiPlayer(
                index, GOOBI_PLAYER_STRING_REP)
            players.append(goobi_player)
        elif player == LEARNING_PLAYER_INDEX:
            learning_player = learningAgent.ValueIterationPlayer(
                index, LEARNING_PLAYER_STRING_REP)
            players.append(learning_player)
        elif player == HEURISTIC_PLAYER_INDEX:
            heuristic_player = HeuristicPlayer.HeuristicPlayer(
                index, HEURISTIC_PLAYER_STRING_REP)
            players.append(heuristic_player)
        elif player == AZULAY_PLAYER_INDEX:
            azulay_player = AzulayPlayer.AzulayPlayer(
                index, AZULAY_PLAYER_STRING_REP)
            players.append(azulay_player)
        elif player == OFIR_PLAYER_INDEX:
            ofir_player = OfirPlayer.OfirPlayer(
                index, OFIR_PLAYER_STRING_REP)
            players.append(ofir_player)
        elif player == HILLEL_PLAYER_INDEX:
            hillel_player = HillelPlayer.HillelPlayer(
                index, HILLEL_PLAYER_STRING_REP)
            players.append(hillel_player)
        elif player == HUMAN_PLAYER_INDEX:
            human_player = HumanPlayer.HumanPlayer(
                index, HUMAN_PLAYER_STRING_REP)
            players.append(human_player)
        elif player == RANDOM_PLAYER_INDEX:
            random_player = RandomPlayer.RandomPlayer(
                index, RANDOM_PLAYER_STRING_REP)
            players.append(random_player)
        elif player == EXPECTI_PLAYER_INDEX:
            expecti_player = ExpectiPlayer.ExpectiPlayer(
                index, EXPECTI_PLAYER_STRING_REP)
            players.append(expecti_player)
        elif player == TSCORING_PLAYER_INDEX:
            tscoring_player = TScoringPlayer.TScoringPlayer(
                index, TSCORING_PLAYER_STRING_REP)
            players.append(tscoring_player)
        elif player == END_RACE_PLAYER_INDEX:
            end_race_player = EndRacePlayer.EndRacePlayer(
                index, END_RACE_PLAYER_STRING_REP)
            players.append(end_race_player)
        elif player == QLEARNING_PLAYER_INDEX:
            q_player = QLearningAgent.QLearningAgent(
                index, QLEARNING_PLAYER_STRING_REP)
            players.append(q_player)
        elif player == APPROX_QLEARNING_PLAYER_INDEX:
            approx_q_player = ApproxQLearningAgent.ApproxQLearningAgent(
                index, APPROX_QLEARNING_STRING_REP)
            players.append(approx_q_player)

    return players

"""
This function is the main function which get the user input values and create
a pig game object according to the input of the user.
"""


def main():
    # Check that the user entered a valid number of input values and notify
    # the user if he didn't.
    if len(sys.argv) != 5:
        print("Invalid Input\nUsage: <player1,player2,...,playerN> "
              "<Shuffle Bit> <Print Mode> <Num of Games>\n")
        print("Players Indexes: ")
        print("0 - Goobi player\n1 - Learning player\n2 - Heuristic player\n"
              "3 - Azulay player\n4 - Ofir player\n5 - Hillel player\n"
              "6 - Human player\n7 - Random player\n8 - Expecti player\n"
              "9 - TScoring Player\n10 - End Race player\n 11 - Q Player\n"
              "12 - Approx Q Player")
        return
    # get the input values
    players = get_players()
    number_of_games = int(sys.argv[4])
    shuffle_mode = sys.argv[2]
    for i in range(number_of_games):
        if i % 10000 == 0 and i != 0:
            print(i)
        if int(sys.argv[2]):
            shuffle(players)
            # Create a pig game object and run the game
        pig = PigGame(100, players)
        pig.run_game()

    print()
    print("Game results: ")
    if int(shuffle_mode):
        print("Shuffle mode is on")
        print()
    # sort the player's scores and print it.
    players.sort(key=lambda x: x.get_wins(), reverse=True)
    for index, player in enumerate(players):
        print(player.get_name() + " won " + str(player.get_wins()) + " games "
              + "(" + str(100 * player.get_wins() / number_of_games) + "%)")

if __name__ == "__main__":
    main()
