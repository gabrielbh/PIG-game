from AbstractPlayer import AbstractPlayer

PRE_TURN_SCORE_IDX = 0
CUR_TURN_SCORE_IDX = 2
EPSILON = 0.00001
OPPONENT_IDX = 1
DISCOUNT_FACTOR = 1


class ValueIterationPlayer(AbstractPlayer):

    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        super(ValueIterationPlayer, self).__init__(index, name, goal_score,
                                                   max_dice_value)

        self.table = self.states_table()
        self.update_table()

    """
    returns a table with the value of each state.
    """
    def states_table(self):
        states_table = {}
        for i in range (107):
            for j in range(107):
                for k in range (107):
                    states_table[(i, j, k)] = 0
        return states_table

    def reward(self, state1, state2):
        goal = 100
        if state2[PRE_TURN_SCORE_IDX] < state1[PRE_TURN_SCORE_IDX]:
            return 0
        if state1[PRE_TURN_SCORE_IDX] + state1[CUR_TURN_SCORE_IDX] < goal \
                and state2[PRE_TURN_SCORE_IDX]\
                        + state2[CUR_TURN_SCORE_IDX] >= goal:
            return 1
        else:
            return 0

    def value_iteration(self, states):
        delta = 1
        while (delta >= EPSILON):
            delta = 0
            for state in states:
                v = self.table[state]
                myScore = state[PRE_TURN_SCORE_IDX]
                hisScore = state[OPPONENT_IDX]
                turnScore = state[CUR_TURN_SCORE_IDX]

                roll_result = 0
                for myNext in range(turnScore + 2, turnScore + 7):
                    next_state = (myScore, hisScore, myNext)
                    roll_result += 1/6 * (self.reward(state, next_state)
                                          + DISCOUNT_FACTOR *
                                          self.table[next_state])
                one_roll_state = (hisScore, myScore, 0)
                roll_result += 1/6 * (DISCOUNT_FACTOR *
                                      (1 - self.table[one_roll_state]))
                hold_result = 1 - self.table[
                    (hisScore, myScore + turnScore, 0)]
                self.table[state] = max(roll_result, hold_result)
                delta = max(delta, abs(v - self.table[state]))

    def update_table(self):
        print("Loading Learning Agent")
        score = 198
        to_print = 10
        while score >= 0:
            score_list = []
            for i in range(99, -1, -1):
                j = score - i
                if j > 99 or j < 0:
                    continue
                for k in range(100 - i):
                    if k == 1:
                        continue
                    state = (i, j, k)
                    score_list.append(state)
            percentage = 100 - (score / 198) * 100
            if int(percentage) % to_print == 0 and int(percentage) != 0:
                print(str(int(percentage)) + "%")
                to_print += 10

            self.value_iteration(score_list)
            score -= 1

        for myTotScore in range(107):
            for anOpponentScore in range(107):
                for aTurnScore in range(107):
                    if myTotScore + aTurnScore >= 100 or myTotScore >= 100:
                        self.table[(myTotScore, anOpponentScore, aTurnScore)]\
                            = 1

    def play(self, game_state, turn_score):
        my_score = game_state[self.index]
        his_score = 0
        for key,value in game_state.items():
            if key != self.index and value > his_score:
                his_score = value

        if my_score + turn_score >= 100:
            return False

        roll_val = 0
        for curTurnScore in range(turn_score + 2, turn_score + 7):
            roll_val += 1/6 * (self.table[(my_score, his_score, curTurnScore)])
        one_roll_state = (his_score, my_score, 0)
        roll_val += 1/6 * (1 - self.table[one_roll_state])
        hold_state = (his_score, my_score + turn_score, 0)
        hold_val = 1 - self.table[hold_state]

        if roll_val >= hold_val:
            return True
        return False
