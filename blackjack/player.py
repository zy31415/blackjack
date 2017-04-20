class Player(object):
    def __init__(self):
        self.sum = None
        self.usable_ace = None
        self._has_stuck = None
        self.faceup = None
        self.history = None
        self.reward = None

    def init(self, faceup, card1, card2):
        self.reward = None
        self.faceup = faceup

        self.sum = 0
        self.usable_ace = False
        self._has_stuck = False
        self.history = []

        self._add(card1)
        self._add(card2)

    def if_hit(self):
        assert not self._has_stuck, "You have decided to stick."

        # No hit when busted.
        if self.if_busted():
            return False

        return self.hit_strategy()

    def hit(self, card):
        '''
        :param card: Card a player get when hit
        :return: True - Not busted. False: this player goes busted.
        '''
        assert not self._has_stuck, "You have decided to stick."
        self._record_history(if_hit=True)
        self._add(card)

    def stick(self):
        self._record_history(if_hit=False)
        self._has_stuck = True

    def _add(self, card):
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

    def _record_history(self, if_hit):
        self.history.append((self.usable_ace, self.sum, if_hit))

    def hit_strategy(self):
        '''
        Make the decision whether to stick (return True) or not (return False)
        :return: bool 
        '''
        return self.sum < 20

    def if_busted(self):
        return self.sum > 21

    def finish(self, reward):
        self.reward = reward

    def iterate_valid_history(self):
        '''
        Iterate history records that are counted as a state. i.e. when sum < 12 or sum > 21 is not counted as a state.
        :return: 
        '''
        for has_usable_ace, sum, if_hit in self.history:
            if 12 <= sum <= 21:
                yield has_usable_ace, sum, if_hit


class Dealer(Player):
    def __init__(self):
        super().__init__()

    def hit_strategy(self):
        return self.sum < 17


