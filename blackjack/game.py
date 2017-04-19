import random


class Player(object):
    def __init__(self, faceup=None):
        self.sum = 0
        self.usable_ace = False
        self._if_stick = False
        self.faceup = faceup

    def if_stick(self):
        if not self._if_stick:
            # get the action: whether to stick or not
            self._if_stick = self.stick_strategy()

        return self._if_stick

    def hit(self, card):
        '''
        :param card: Card a player get when hit
        :return: True - Not busted. False: this player goes busted.
        '''

        # When sum <= 10, treat card 1 as 11 and set usable_ace to True
        if card == 1 and self.sum <= 10:
            self.sum += 11
            self.usable_ace = True
        else:
            self.sum += card

        # If sum is greater than 21, then check if the sum contains a usable ace. If Yes, count that usable ace as 1.
        if self.sum > 21 and self.usable_ace:
            self.sum -= 10
            self.usable_ace = False

        return self.sum <= 21

    def stick_strategy(self):
        '''
        Make the decision whether to stick (return True) or not (return False)
        :return: bool 
        '''
        return self.sum >= 20

    def if_busted(self):
        return self.sum > 21


class Dealer(Player):
    def __init__(self):
        super().__init__()

    def stick_strategy(self):
        return self.sum >= 17


class Game(object):
    def __init__(self, player_class = Player, player_class_kwargs = {}):
        self.dealer = None
        self.faceup = None

        self.player = None
        self.player_class = player_class
        self.player_class_kwargs = player_class_kwargs

        self.player_history = None
        self.verbose = True

    @staticmethod
    def draw():
        card = random.randint(1, 13)
        return card if card < 10 else 10

    def init(self):
        if self.verbose:
            print('Game start.')

        self.player_history = []

        self.dealer = Dealer()

        self.faceup = self.draw()

        self.dealer.hit(self.faceup)
        self.dealer.hit(self.draw())

        self.player = self.player_class(faceup=self.faceup, **self.player_class_kwargs)
        self.player.hit(self.draw())
        self.player.hit(self.draw())

        self._record_player_history()

        if self.verbose:
            print('  Init:')
            print('    Faceup: %d, %s' % (self.faceup, self._str_players_status()))

    def play(self):
        # when player has a natural:
        if self.player.sum == 21:
            reward = 0 if self.dealer.sum == 21 else 1
            if self.verbose:
                print('Game over.')
                print('  Player has a natural. Reward: %d.' % reward)
            return reward

        if self.verbose:
            print("  Player's Round:")

        while not self.player.if_stick():
            _draw = self.draw()
            self.player.hit(_draw)
            self._record_player_history()
            if self.verbose:
                print("    " + "Draw %d, " % _draw + self._str_players_status())

        if self.player.if_busted():
            if self.verbose:
                print('Game Over. Player is lost. He is busted')
            return -1

        if self.verbose:
            print("  Dealer's Round:")

        while not self.dealer.if_stick():
            _draw = self.draw()
            self.dealer.hit(_draw)
            if self.verbose:
                print("    " + "Draw %d, " % _draw + self._str_players_status())

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

    def _record_player_history(self):
        self.player_history.append((self.player.usable_ace, self.player.sum))


if __name__ == '__main__':
    game = Game()
    game.init()
    print(game.play())
    print(game.player_history)




