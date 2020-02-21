import env
from env import *
import numpy as np

Q = np.zeros((210, 2))



numEpisodes = 100000
decayFactor = .9999

done = False
lr = .99
epsilon = .5
state = [0, 0]

def e_greedy(eps, Q, state):
    if np.random.random() < eps or np.sum(Q[state:, ]) == 0:
        action = np.random.randint(0, 2)
    elif state < 12:
        action = 0
    else:
        action = np.argmax(Q[state,])
    return action

rAll = 0
rFirstHalf = 0
rSecondHalf = 0

for i in range(numEpisodes):
    r = 0
    state[1], state[0] = env.startGame()


    stateNum = ((state[1] - 1) * 10) + (state[0] - 1)

    a = e_greedy(epsilon, Q, stateNum)

    d = False

    while not d:

        print("state", state)

        state1, r, d = env.step(state, a)

        if state[1] > 21:
            break

        print("state1", state1)

        stateNum1 = ((state1[1] - 1) * 10) + (state1[0] - 1)


        a1 = e_greedy(epsilon, Q, stateNum1)


        Q[stateNum, a] = Q[stateNum, a] + lr * (r + (Q[stateNum1, a1] - Q[stateNum, a]))

        state = state1
        stateNum = stateNum1

        a = a1

    epsilon = epsilon * decayFactor




    print("---------")
    rAll = rAll + r

    if i < numEpisodes / 2:
        rFirstHalf += r
    else:
        rSecondHalf += r



print(Q)
print("Average Reward:", rAll / numEpisodes)
print("First Half Average Reward:", rFirstHalf / (numEpisodes / 2))
print("Second Half Average Reward:", rSecondHalf / (numEpisodes / 2))









