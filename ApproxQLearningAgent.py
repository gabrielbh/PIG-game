from AbstractPlayer import AbstractPlayer
import ExpectiPlayer
import random
import numpy
import util
import featureExtractors

PRE_TURN_SCORE_IDX = 0
CUR_TURN_SCORE_IDX = 2
ITER = 100000
ALPHA_INITIAL_VALUE = 1
ALPHA_DECAY_RATE = 0.999


class ApproxQLearningAgent(AbstractPlayer):

    def __init__(self, index, name, goal_score=100, max_dice_value=6):
        self.index = index
        self.discount = 1
        self.weights = util.Counter()  # A Counter is a dict with default 0
        self.score = 0
        self.num_of_throws = 0
        self.goal_score = goal_score
        self.max_dice_value = max_dice_value
        self.name = name
        self.wins = 0
        self.table = self.statesTable()
        self.counter = self.counter_table()
        self.opponent = ExpectiPlayer.ExpectiPlayer(0, "Expecti Player")
        self.train(1, 0.1)


    def statesTable(self):
        states_table = {}
        for i in range (107):
            for j in range(107):
                for k in range (107):
                    states_table[(i, j, k)] = 0
        return states_table

    def counter_table(self):
        counter_table = {}
        for state in self.table:
            for i in range(2):
                counter_table[(state, i)] = 0
        return counter_table

    def reward(self, state1, state2):
        goal = 100
        if state2[PRE_TURN_SCORE_IDX] < state1[PRE_TURN_SCORE_IDX]:
            return 0
        if state1[PRE_TURN_SCORE_IDX] + state1[CUR_TURN_SCORE_IDX] < goal <= \
                        state2[PRE_TURN_SCORE_IDX] + \
                        state2[CUR_TURN_SCORE_IDX]:
            return 1
        else:
            return 0

    def train(self, discount_factor, epsilon):
        alpha = ALPHA_INITIAL_VALUE

        for i in range(ITER):
            if i % 10000 == 0:
                print(i)
            state = (0, 0, 0)
            while state[0] + state[2] < 100 and state[1] < 100:

                opponent_score = 0
                while self.opponent.play(state, opponent_score) and opponent_score + state[1] < 100:
                    roll = random.randint(1, 6)
                    if roll != 1:
                        opponent_score += roll
                    else:
                        opponent_score = 0
                        break

                random_action = numpy.random.binomial(1, epsilon)

                hold_q_val, roll_q_val = 0, 0

                if random_action:
                    decision = random.randint(0, 1)

                else:
                    # Hold
                    hold_q_val = self.getQValue((state[0] + state[2], state[1] + opponent_score, 0), 0)

                    # roll
                    roll_q_val = 0
                    for roll in range(2, 7):
                        roll_next_state = (state[0], state[1], state[2] + roll)
                        roll_q_val += 1/6 * self.getQValue(roll_next_state, 1)
                    roll_q_val += 1/6 * self.getQValue((state[0], state[1] + opponent_score, 0), 1)

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
                    next_state = (state[0] + state[2], state[1] + opponent_score, 0)

                reward = self.reward(state, next_state)

                self.counter[(state, decision)] += alpha * (reward + discount_factor * max(hold_q_val, roll_q_val) - self.getQValue(state, decision))

                if next_state[2] >= 100:
                    break

                self.update(state, decision, next_state, reward, 0.99)

                state = next_state

            alpha = ALPHA_DECAY_RATE * alpha

    def getQValue(self, state, action):
        """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
        """
        # According to the formula given in the exercise
        features = featureExtractors.IdentityExtractor().getFeatures(state, action)
        q_val = 0
        for feature in features:
            q_val += features[feature] * self.weights[feature]
        return q_val


    def getValue(self, state):
        opponent_score = 0
        while (self.opponent).play(state, opponent_score) and opponent_score + state[1] < 100:
            roll = random.randint(1, 6)
            if roll != 1:
                opponent_score += roll
            else:
                opponent_score = 0
                break

        # Hold
        hold_q_val = self.counter[((state[0] + state[2], state[1] + opponent_score, 0), 0)]

        # roll
        roll_q_val = 0
        for roll in range(2, 7):
            roll_next_state = (state[0], state[1], state[2] + roll)
            roll_q_val += 1/6 * self.counter[(roll_next_state, 1)]
        roll_q_val += 1/6 * self.counter[((state[0], state[1] + opponent_score, 0), 1)]

        return max(roll_q_val, hold_q_val)

    def getCorrection(self, state, action, nextState, rewrad):
        """
        This function calculates the correction value according to the formula
        given in the exercise
        """
        return rewrad + self.discount * self.getValue(nextState) - \
               self.getQValue(state, action)

    def update(self, state, action, nextState, reward, alpha):
        """
       Should update your weights based on transition
        """
        # Update the weights according to the formula given in the exercise
        features = featureExtractors.IdentityExtractor().getFeatures(state, action)

        for feature in features:
            self.weights[feature] += \
                alpha * \
                self.getCorrection(state, action, nextState, reward) * \
                features[feature]

    def play(self, game_state, turn_score):
        my_score = game_state[self.index]
        hisScore = 0
        for key,value in game_state.items():
            if key != self.index and value > hisScore:
                hisScore = value

        if my_score + turn_score >= 100:
            return False

        opponent_score = 0
        while self.opponent.play(game_state, opponent_score) and opponent_score + hisScore < 100:
            roll = random.randint(1, 6)
            if roll != 1:
                opponent_score += roll
            else:
                break

        rollVal = 0
        for curTurnScore in range(turn_score + 2, turn_score + 7):
            rollVal += 1/6 * (self.getQValue((my_score, hisScore, curTurnScore), 1))
        one_roll_state = (my_score, hisScore + opponent_score, 0)
        rollVal += 1/6 * self.getQValue(one_roll_state, 1)

        hold_state = (my_score + turn_score, hisScore + opponent_score, 0)
        hold_val = self.getQValue(hold_state, 0)

        if turn_score == 0:
            return True

        if rollVal == hold_val:
            return bool(random.randint(0, 1))

        elif rollVal > hold_val:
            return True

        return False
