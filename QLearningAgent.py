from AbstractPlayer import AbstractPlayer
import ExpectiPlayer
import random
import numpy

PRE_TURN_SCORE_IDX = 0
CUR_TURN_SCORE_IDX = 2
ITER = 100000
ALPHA_INITIAL_VALUE = 1
ALPHA_DECAY_RATE = 0.999999


class QLearningAgent(AbstractPlayer):
    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        super(QLearningAgent, self).__init__(index, name, goal_score,
                                             max_dice_value)
        self.table = self.create_states_table()
        self.counter = self.counter_table()
        self.opponent = ExpectiPlayer.ExpectiPlayer(0, "Expecti Player")
        self.train(1, 0.1)


    @staticmethod
    def create_states_table():
        states_table = {}
        for i in range(107):
            for j in range(107):
                for k in range(107):
                    states_table[(i, j, k)] = 0
        return states_table

    @staticmethod
    def reward(state1, state2):
        goal = 100
        if state2[PRE_TURN_SCORE_IDX] < state1[PRE_TURN_SCORE_IDX]:
            return 0
        if state1[PRE_TURN_SCORE_IDX] + state1[CUR_TURN_SCORE_IDX] < goal <= \
                        state2[PRE_TURN_SCORE_IDX] + \
                        state2[CUR_TURN_SCORE_IDX]:
            return 1
        else:
            return 0

    def counter_table(self):
        counter_table = {}
        for state in self.table:
            for i in range(2):
                counter_table[(state, i)] = 0
        return counter_table

    def get_opponent_score(self, state):
        opponent_score = 0
        while self.opponent.play(state, opponent_score) and opponent_score + \
                state[1] < 100:
            roll = random.randint(1, 6)
            if roll != 1:
                opponent_score += roll
            else:
                opponent_score = 0
                break
        return opponent_score

    def train(self, discount_factor, epsilon):
        alpha = ALPHA_INITIAL_VALUE

        for i in range(ITER):
            if i % 10000 == 0:
                print(i)
            state = (0, 0, 0)
            while state[0] + state[2] < 100 and state[1] < 100:

                opponent_score = self.get_opponent_score(state)

                random_action = numpy.random.binomial(1, epsilon)

                if random_action:
                    decision = random.randint(0, 1)

                else:
                    # Hold
                    hold_q_val = self.counter[(
                        (state[0] + state[2], state[1] + opponent_score, 0),
                        0)]

                    # roll
                    roll_q_val = 0
                    for roll in range(2, 7):
                        roll_next_state = (state[0], state[1], state[2] + roll)
                        roll_q_val += 1 / 6 * self.counter[
                            (roll_next_state, 1)]
                    roll_q_val += 1 / 6 * self.counter[
                        ((state[0], state[1] + opponent_score, 0), 1)]

                    if hold_q_val > roll_q_val:
                        decision = 0
                    else:
                        decision = 1

                if decision:
                    roll = random.randint(1, 6)
                    if roll != 1:
                        next_state = (state[0], state[1], state[2] + roll)
                    else:
                        next_state = (state[0], state[1] + opponent_score, 0)

                else:
                    next_state = (
                        state[0] + state[2], state[1] + opponent_score, 0)

                reward = self.reward(state, next_state)

                roll_q_val = self.counter[(next_state, 1)]
                hold_q_val = self.counter[(next_state, 0)]

                self.counter[(state, decision)] += alpha * (
                    reward + discount_factor * max(roll_q_val, hold_q_val) -
                    self.counter[(state, decision)])
                state = next_state

            alpha = ALPHA_DECAY_RATE * alpha

    def play(self, game_state, turn_score):
        my_score = game_state[self.index]
        his_score = 0
        for key, value in game_state.items():
            if key != self.index and value > his_score:
                his_score = value

        if my_score + turn_score >= 100:
            return False

        opponent_turn_score = self.get_opponent_score(game_state)

        opponent_next_turn_score = his_score + opponent_turn_score

        if opponent_next_turn_score >= 107:
            opponent_next_turn_score = 106

        roll_val = 0
        for curTurnScore in range(turn_score + 2, turn_score + 7):
            roll_val += 1 / 6 * (
                self.counter[((my_score, his_score, curTurnScore), 1)])
        one_roll_state = (my_score, opponent_next_turn_score, 0)
        roll_val += 1 / 6 * (self.counter[(one_roll_state, 1)])

        hold_state = (my_score + turn_score, opponent_next_turn_score, 0)
        hold_val = self.counter[(hold_state, 0)]

        if roll_val == hold_val and turn_score != 0:
            return random.randint(0, 1)

        elif roll_val > hold_val:
            return True

        return False
