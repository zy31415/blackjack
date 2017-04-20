import random
from .player import Player, Dealer


class Game(object):
    def __init__(self, player=None):
        self.dealer = None

        self.player = Player() if player is None else player
        self.dealer = Dealer()

        self.verbose = True
        self.faceup = None

    @staticmethod
    def draw():
        card = random.randint(1, 13)
        return card if card < 10 else 10

    def init(self):
        if self.verbose:
            print('Game start.')

        faceup = self.draw()

        self.dealer.init(faceup=faceup, card1=faceup, card2=self.draw())
        self.player.init(faceup=faceup, card1=self.draw(), card2=self.draw())

        if self.verbose:
            print('  Init:')
            print('    Faceup: %d, %s' % (faceup, self._str_players_status()))

        self.faceup = faceup

    def play(self):
        reward = self._play()
        self.player.finish(reward)
        self.dealer.finish(reward)
        return reward

    def _play(self):
        # when player has a natural:
        if self.player.sum == 21:
            reward = 0 if self.dealer.sum == 21 else 1
            if self.verbose:
                print('Game over.')
                print('  Player has a natural. Reward: %d.' % reward)
            return reward

        if self.verbose:
            print("  Player's Round:")

        while True:
            if self.player.if_hit():
                _draw = self.draw()
                self.player.hit(_draw)
                if self.verbose:
                    print("    " + "Draw %d, " % _draw + self._str_players_status())
            else:
                self.player.stick()
                break

        if self.player.if_busted():
            if self.verbose:
                print('Game Over. Player is lost. He is busted')
            return -1

        if self.verbose:
            print("  Dealer's Round:")

        while True:
            if self.dealer.if_hit():
                _draw = self.draw()
                self.dealer.hit(_draw)
                if self.verbose:
                    print("    " + "Draw %d, " % _draw + self._str_players_status())
            else:
                self.dealer.stick()
                break

        if self.dealer.if_busted():
            if self.verbose:
                print('Game Over. Dealer is lost. He is busted')
            return -1

        if self.player.sum == self.dealer.sum:
            if self.verbose:
                print('Game Over. Tie.')
            return 0

        if 21 - self.player.sum < 21 - self.dealer.sum:
            if self.verbose:
                print('Game Over. Player wins.')
            return 1

        if self.verbose:
            print('Game Over. Dealer wins.')

        return -1

    def _str_players_status(self):
        da = "(A)" if self.dealer.usable_ace else ""
        pa = "(A)" if self.player.usable_ace else ""
        return "Dealer: %d%s, Player: %d%s" % (self.dealer.sum, da, self.player.sum, pa)

