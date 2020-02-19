import numpy as np
import random
from random import seed

def drawCard():

    seed()


    return random.randint(1,10), random.randint(0, 2)

def step(s, a):

    dealerVal = s[0]
    if a == 0:
        card, color = drawCard()


        if color == 1 or color == 2: #black
            s[1] = s[1] + card

        else: #red
            s[1] = s[1] - card

    else:
        while dealerVal < 17:
            card, color = drawCard()
            if color == 1 or color == 2:
                dealerVal = dealerVal + card
            else:
                dealerVal = dealerVal - card

    reward = checkWinner(s[1], dealerVal, s[0])


    if reward == 2:
        done = False
    else:
        done = True

    return s, reward, done





def checkWinner(playerVal, dealerVal, dealerInit):
    if playerVal > 21 or playerVal < 1:
        return -1 #dealerwin
    elif dealerVal > 21:
        return 1 #playerwin
    elif dealerVal == dealerInit: #game is not over
        return 2
    elif playerVal > dealerVal:
        return 1
    elif dealerVal > playerVal:
        return -1
    else:
        return 0

def startGame():

    card, color = drawCard()

    playerVal = card

    card, color = drawCard()

    dealerVal = card


    return playerVal, dealerVal










