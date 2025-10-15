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