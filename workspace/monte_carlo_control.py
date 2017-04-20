import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pylab as plt

from blackjack.game import Game
from blackjack.monte_carlo_agent import MCAgent


player = MCAgent()
game = Game(player=player)
game.verbose = False

episodes = 500000

for n in range(episodes):
    game.init()
    game.play()

print(player.policy)
print(player.counts)

faceup = range(1, 11)
sum = range(12, 22)

X, Y = np.meshgrid(sum, faceup)

fig = plt.figure()

ax = fig.add_subplot(121)
ax.imshow(player.policy[0])


ax = fig.add_subplot(122)
cax = ax.pcolor(player.policy[1])
ax.set_aspect('equal')
fig.colorbar(cax)

plt.show()


#ax = fig.add_subplot(111, projection='3d')
#ax.set_aspect('equal')
#ax.plot_wireframe(X, Y, mc.qvalues[0], label='No Usable Ace')
#ax.plot_wireframe(X, Y, mc.qvalues[1], color='red', label='Usable Ace')
#
#ax.set_zlim(-1, 1)
#ax.set_xticks(sum)
#ax.set_yticks(faceup)
#
#ax.set_xlabel("Player Sum")
#ax.set_ylabel("Dealer Showing")
#
#ax.azim = -127
#ax.elev = 32

#plt.legend()

#plt.grid()

#plt.show()
