import random


class Player(object):
    def __init__(self):
        self.sum = 0
        self.usable_ace = False
        self._if_stick = False

    def if_stick(self):
        if not self._if_stick:
            # get the action: whether to stick or not
            self._if_stick = self.stick_strategy()

        return self._if_stick

    def hit(self, card):
        '''
        :param card: Car a player get when hit
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
    def __init__(self):
        self.dealer = None
        self.faceup = None

        self.player = None

        self.verbose = True

    @staticmethod
    def draw():
        return random.randint(1, 10)

    def init(self):
        if self.verbose:
            print('Game start.')
        self.dealer = Dealer()
        self.player = Player()

        self.faceup = self.draw()

        self.dealer.hit(self.faceup)
        self.dealer.hit(self.draw())

        self.player.hit(self.draw())
        self.player.hit(self.draw())

        if self.verbose:
            print('  Init:')
            print('    Faceup: %d, Dealer: %d, Player: %d' % (self.faceup, self.dealer.sum, self.player.sum))

    def play(self):
        # when player has a natural:
        if self.player.sum == 21:
            reward = 0 if self.dealer.sum == 21 else 1
            if self.verbose:
                print('Game over.')
                print('  Player has a natural. Reward: %d.' % reward)
            return reward

        while not self.player.if_stick():
            self.player.hit(self.draw())

        if self.verbose:
            print("  Player's Round:")
            print('    Dealer: %d, Player: %d' % (self.dealer.sum, self.player.sum))

        if self.player.if_busted():
            if self.verbose:
                print('Game Over. Player is lost. He is busted')
            return -1

        while not self.dealer.if_stick():
            self.dealer.hit(self.draw())

        if self.verbose:
            print("  Dealer's Round:")
            print('    Dealer: %d, Player: %d' % (self.dealer.sum, self.player.sum))

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


if __name__ == '__main__':
    game = Game()
    game.init()
    print(game.play())




