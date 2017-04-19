import numpy as np

from .game import Game


class MonteCarloPolicyEvaluation(object):

    def __init__(self):
        self.game = Game()
        self.game.verbose = False

        self.values = np.full((2, 10, 10), np.nan, float)

        self.counts = np.zeros((2, 10, 10), int)

    def evaluate(self, episodes=10000):
        for ii in range(episodes):
            self.do_one_episode()

    def do_one_episode(self):
        self.game.init()
        reward = self.game.play()

        faceup = self.game.faceup
        history = self.game.player_history

        for ace, sum in history:
            if sum < 12 or sum > 21:
                # The policy for sum < 12 is always to hit, thus don't include here.
                continue

            ace_idx = int(ace)
            faceup_idx = faceup - 1
            sum_idx = sum - 12

            val = self.values[ace_idx, faceup_idx, sum_idx]
            count = self.counts[ace_idx, faceup_idx, sum_idx]

            if count == 0:
                self.values[ace_idx, faceup_idx, sum_idx] = reward
                self.counts[ace_idx, faceup_idx, sum_idx] = 1
            else:
                self.values[ace_idx, faceup_idx, sum_idx] = (val * count + reward) / (count + 1)
                self.counts[ace_idx, faceup_idx, sum_idx] = count + 1

if __name__ == '__main__':
    mc = MonteCarloPolicyEvaluation()

    mc.evaluate()
