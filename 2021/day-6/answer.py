import os
from collections import defaultdict

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [list(map(int, line.split(","))) for line in inputFile.readlines()][0]

CHILDBIRTH_CYCLE = 7
CHILDBIRTH_BIRTH_DELAY = 2


class Sea(object):
    def __init__(self, fishes):
        self.generations = []
        self.fishesByChildbirthDaysLeft = defaultdict(int)
        for fish in fishes:
            self.fishesByChildbirthDaysLeft[fish] += 1
        self.generations.append(self.fishesByChildbirthDaysLeft)

    def nextDay(self):
        newDay = defaultdict(int)
        for childBirthDayLeft, amount in self.fishesByChildbirthDaysLeft.items():
            newDay[childBirthDayLeft - 1] = amount
        eggs = newDay[-1]
        newDay[CHILDBIRTH_CYCLE - 1] += eggs
        newDay[CHILDBIRTH_CYCLE + CHILDBIRTH_BIRTH_DELAY - 1] += eggs
        newDay.pop(-1)
        self.generations.append(newDay)
        self.fishesByChildbirthDaysLeft = newDay

    def countFishes(self):
        return sum(self.fishesByChildbirthDaysLeft.values())


class Lanternfish(object):
    def __init__(self, initialValue):
        self.value = initialValue

    def nextDay(self):
        self.value -= 1
        if self.value == -1:
            self.value = CHILDBIRTH_CYCLE - 1
            return self.createEgg()

    def createEgg(self):
        return Lanternfish(CHILDBIRTH_CYCLE + CHILDBIRTH_BIRTH_DELAY - 1)

    def __int__(self):
        return self.value

    def __str__(self):
        return str(int(self))


def displayFishes(day, fishes):
    print("After %s day: %s" % (day, ",".join(str(fish) for fish in fishes)))


def answer1(numbers, days):
    lanternfishes = [Lanternfish(number) for number in numbers]
    for day in range(days):
        eggs = []
        # displayFishes(day, lanternfishes)
        for lanternfish in lanternfishes:
            egg = lanternfish.nextDay()
            if egg:
                eggs.append(egg)
        lanternfishes.extend(eggs)
        print("%s / %s" % (day + 1, days))
    # displayFishes(days, lanternfishes)
    return len(lanternfishes)


def answer2(numbers, days):
    sea = Sea(numbers)
    for day in range(days):
        sea.nextDay()
        print("%s / %s : %s" % (day + 1, days, sea.countFishes()))
    return sea.countFishes()

print(answer1(lines, days=80))
print(answer2(lines, days=256))
