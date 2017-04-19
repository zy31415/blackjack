import numpy as np

from .game import Game, Player


class PlayerAgent(Player):

    def __init__(self, faceup, policy):
        super().__init__(faceup=faceup)
        self.policy = policy

    def stick_strategy(self):
        return not self.policy[int(self.usable_ace), self.faceup, self.sum]


class MonteCarloControl(object):
    def __init__(self):

        # State(if has ace, faceup, sum) and action (hit or stick)
        self.qvalues = np.full((2, 10, 10, 2), np.nan, float)

        self.counts = np.zeros((2, 10, 10, 2), int)

        # True - hit, False - stick
        self.policy = np.full((2, 10, 10), True, bool)

        self.game = Game(player_class=PlayerAgent, player_class_kwargs={'policy', self.policy})
        self.game.verbose = False

    def do_one_episode(self):
        self.game.init()


