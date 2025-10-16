import random as rand

def choiceSleepTime():
    timeFuncs = [lambda: 3.25 + rand.random(),
         lambda: 5 + rand.random() * 5,
         lambda: 10 + rand.random() * 10,
         lambda: 20 + rand.random() * 7 * rand.choice([1, -1]),
         lambda: 180 + rand.random() * rand.choice([15, 20, 25]) * rand.choice([1, -1])]
    funcsWeights = [0.1, 0.45, 0.34, 0.1, 0.01]
    return rand.choices(timeFuncs, funcsWeights, k = 1)[0]()

def getCardinalNumeralEnding(number):
    lastDigit = number % 10
    if lastDigit == 1:
        if number % 100 != 11:
            return 0
        else:
            return 2
    elif lastDigit in (2, 3, 4):
        return 1
    else:
        return 2