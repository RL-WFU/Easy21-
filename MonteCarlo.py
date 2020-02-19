import env
from env import *
import numpy as np


N = np.zeros((100, 2))
Q = np.zeros((100, 2))

num_episodes = 20000



lr = .8

rAll = 0


for i in range(num_episodes):

    s = [0, 0]
    done = False
    r = 0

    s[1], s[0] = env.startGame()


    while not done:

        if s[1] < 12:
            s, r, done = env.step(s, 0)

        else:
            print(s[1], s[0])

            stateNumOld = ((s[1] - 12) * 10) + (s[0] - 1)

            a = np.argmax(Q[stateNumOld, ])

            s, r, done = env.step(s, a)

            if s[1] >= 21:
                break

            print(s)

            stateNum = ((s[1] - 12) * 10) + (s[0] - 1)

            print(stateNum, stateNumOld)

            N[stateNum, a] = N[stateNum, a] + 1

            Q[stateNum, a] = r + Q[stateNum, a]

    rAll = rAll + r


print(rAll / num_episodes)








