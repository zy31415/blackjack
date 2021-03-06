from blackjack import MCPolicyEvaluationAgent, Game

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pylab as plt
import numpy as np


player = MCPolicyEvaluationAgent()

game = Game(player=player)
game.verbose = False

for n in range(200000):
    game.init()
    game.play()

print(player.values)
print(player.counts)

faceup = range(1, 11)
sum = range(12, 22)

X, Y = np.meshgrid(sum, faceup)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.plot_wireframe(X, Y, player.values[0], label='No Usable Ace')
ax.plot_wireframe(X, Y, player.values[1], color='red', label='Usable Ace')
ax.set_zlim(-1, 1)
ax.set_xticks(sum)
ax.set_yticks(faceup)

ax.set_xlabel("Player Sum")
ax.set_ylabel("Dealer Showing")

ax.azim = -127
ax.elev = 32

plt.legend()

plt.grid()

plt.show()
