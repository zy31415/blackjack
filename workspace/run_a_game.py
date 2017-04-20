from blackjack import Game


game = Game()

game.verbose = True

game.init()
game.play()

print(game.player.history)
print(game.dealer.history)