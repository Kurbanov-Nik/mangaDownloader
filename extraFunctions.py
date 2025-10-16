import random as rand

def choiceSleepTime(longSleep = False):
    timeRandomizer = {
        False: [
            lambda: 3.25 + rand.random(),
            lambda: 5 + rand.random() * 5,
            lambda: 10 + rand.random() * 10 - rand.random() * 3],
        True: [
            lambda: 60 + rand.random() * 2 + rand.random() * 10 * rand.choice([1, -1]),
            lambda: 32.5 + rand.random() * rand.choice([15, 20, 25])]}
    weights = {
        False: [0.30, 0.55, 0.15],
        True: [0.4, 0.6]}
    return rand.choices(timeRandomizer[longSleep], weights[longSleep], k = 1)[0]()

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