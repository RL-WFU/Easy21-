import env
import numpy as np


features = [0] * 36
parameters = [0.5] * 36

epsilon = .5

decayFactor = .9999

stepSize = .01

numEpisodes = 50000

lr = .8

state = [0, 0]

dealerIntervals = ([1, 2, 3 ,4], [4, 5, 6, 7], [7, 8, 9, 10])
playerIntervals = ([1, 2, 3, 4, 5, 6], [4, 5, 6, 7, 8, 9], [7, 8, 9, 10, 11, 12], [10, 11, 12, 13, 14, 15], [13, 14, 15, 16, 17, 18], [16, 17, 18, 19, 20, 21])


def calcFeatureNum(playerSum, dealerFirst, action):
    dOverlap = False
    pOverlap = False
    dealerInt = -1
    playerInt = -1
    i = 0
    for interval in dealerIntervals:

        if dealerFirst in interval:
            dealerInt = i  # 0 - 2

            if i != 2:
                if dealerFirst in dealerIntervals[dealerInt + 1]:
                    dOverlap = True

            break

        i = i + 1

    i = 0
    for interval in playerIntervals:

        if playerSum in interval:
            playerInt = i  # 0 - 5

            if i != 5:
                if playerSum in playerIntervals[playerInt + 1]:
                    pOverlap = True

            break

        i = i + 1

    featureNum = (6 * dealerInt) + playerInt + (18 * action)

    if featureNum < 0:
        print("error")

    featureNum2 = -1

    if dOverlap and pOverlap:
        featureNum2 = featureNum + 7
    elif dOverlap:
        featureNum2 = featureNum + 6
    elif pOverlap:
        featureNum2 = featureNum + 1

    return featureNum, featureNum2



def fillFeatureVector(featureNum, featureNum2, x):
    for i in range(36):
        x[i] = 0

    x[featureNum] = 1
    if featureNum2 != -1:
        x[featureNum2] = 1

    return x





def eGreedy(eps, playerSum, dealerFirst, parameters):
    if np.random.random() < eps:
        action = np.random.randint(0, 2)

    else:
        featureNumStick, featureNum2Stick = calcFeatureNum(playerSum, dealerFirst, 0)

        featureNumHit, featureNum2Hit = calcFeatureNum(playerSum, dealerFirst, 1)

        if featureNum2Stick == -1: #if no overlap (shouldn't be overlap in both cases stick and hit if one is no overlap)
            if parameters[featureNumStick] == parameters[featureNumHit]:
                action = np.random.randint(0, 2)
            elif parameters[featureNumStick] > parameters[featureNumHit]:
                action = 0
            else:
                action = 1
        else:
            if parameters[featureNumStick] + parameters[featureNum2Stick] == parameters[featureNumHit] + parameters[featureNum2Hit]:
                action = np.random.randint(0, 2)
            elif parameters[featureNumStick] + parameters[featureNum2Stick] > parameters[featureNumHit] + parameters[featureNum2Hit]:
                action = 0
            else:
                action = 1

    return action

def calculateQ(x, w):
    Q = 0
    for i in range(36):
        Q = Q + (x[i] * w[i])

    return Q


def updateParameters(stepSize, reward, lr, features1, features, parameters):
    updateScalar = stepSize * (reward + (lr * calculateQ(features1, parameters) - calculateQ(features, parameters)))
    update = [0] * 36
    for i in range(36):
        update[i] = updateScalar * features[i]
        parameters[i] = parameters[i] + update[i]

    return parameters


rAll = 0
rFirstHalf = 0
rSecondHalf = 0

for i in range(numEpisodes):

    done = False
    reward = 0

    playerSum, dealerFirst = env.startGame()

    a = eGreedy(epsilon, playerSum, dealerFirst, parameters)

    featureNum, featureNum2 = calcFeatureNum(playerSum, dealerFirst, a)

    features = fillFeatureVector(featureNum, featureNum2, features)

    while not done:

        s = [dealerFirst, playerSum]
        s1, reward, done = env.step(s, a)

        playerSum1 = s1[1]
        dealerFirst1 = s1[0]

        if playerSum1 > 21:
            break

        a1 = eGreedy(epsilon, playerSum1, dealerFirst1, parameters)

        featureNumNew, featureNum2New = calcFeatureNum(playerSum1, dealerFirst1, a1)

        features1 = fillFeatureVector(featureNumNew, featureNum2New, features)

        parameters = updateParameters(stepSize, reward, lr, features1, features, parameters)

        playerSum = playerSum1
        dealerFirst = dealerFirst1
        a = a1

    print("-------------")
    rAll = rAll + reward

    if i < numEpisodes / 2:
        rFirstHalf = rFirstHalf + reward
    else:
        rSecondHalf = rSecondHalf + reward

    epsilon = epsilon * decayFactor


print("Total Average Reward:", rAll / numEpisodes)
print("First half average reward:", rFirstHalf / (numEpisodes / 2))
print("Second half average reward:", rSecondHalf / (numEpisodes / 2))

parameters1 = [0] * 18
parameters2 = [0] * 18
for i in range(18):
    parameters1[i] = parameters[i]
    parameters2[i] = parameters[i + 18]

print("Parameters:", parameters)
print("First half parameters:", parameters1)
print("Second half parameters:", parameters2)






