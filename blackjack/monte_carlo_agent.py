import random

import numpy as np

from .player import Player


class MCAgent(Player):

    def __init__(self):
        super().__init__()

        # (ace, faceup, sum)
        self.policy = np.full((2, 10, 10), True, bool)

        # State(if has ace, faceup, sum) and action (hit or stick)
        self.qvalues = np.full((2, 10, 10, 2), np.nan, float)
        self.counts = np.zeros((2, 10, 10, 2), int)

        self.epsilon = 0.1

    def hit_strategy(self):
        sum_idx = self.sum - 12
        faceup_idx = self.faceup - 1
        action = self.policy[int(self.usable_ace), faceup_idx, sum_idx]

        # Most times follow the policy - exploit
        # but some times try other actions - explore
        if random.uniform(0, 1) < self.epsilon:
            return not action

        return action

    def finish(self, reward):
        faceup_idx = self.faceup - 1

        # policy evaluation:
        for ace, sum, if_hit in self.iterate_valid_history():
            sum_idx = sum - 12
            _idx = int(ace), faceup_idx, sum_idx, int(if_hit)
            count = self.counts[_idx]
            val = self.qvalues[_idx]

            self.qvalues[_idx] = reward if np.isnan(val) else (count * val + reward)/(count + 1)
            self.counts[_idx] = count + 1

        # policy update:
        for ace, sum, _ in self.iterate_valid_history():
            sum_idx = sum - 12
            assert sum_idx >= 0
            _q = self.qvalues[int(ace), faceup_idx, sum_idx, :]
            if not np.isnan(_q).all():
                self.policy[int(ace), faceup_idx, sum_idx] = bool(np.nanargmax(_q))
