import numpy as np

from .player import Player


class MCPolicyEvaluationAgent(Player):
    def __init__(self):
        super().__init__()

        self.values = np.full((2, 10, 10), np.nan, float)
        self.counts = np.zeros((2, 10, 10), int)

    def finish(self, reward):
        faceup = self.faceup
        history = self.history

        for ace, sum, _ in self.iterate_valid_history():
            faceup_idx = faceup - 1
            sum_idx = sum - 12
            _idx = int(ace), faceup_idx, sum_idx

            val = self.values[_idx]
            count = self.counts[_idx]

            if count == 0:
                self.values[_idx] = reward
                self.counts[_idx] = 1
            else:
                self.values[_idx] = (val * count + reward) / (count + 1)
                self.counts[_idx] = count + 1


