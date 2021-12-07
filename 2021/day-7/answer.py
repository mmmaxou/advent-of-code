import os
from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    lines = [list(map(int, line.split(","))) for line in inputFile.readlines()][0]


def computeMedian(data):
    dataSorted = sorted(i for i in data)
    mid = len(dataSorted) // 2
    return (dataSorted[mid] + dataSorted[~mid]) / 2


def distance(num, center):
    return sum(range(abs(num - center) + 1))


def computeFuel(numbers, center):
    return sum(distance(num, center) for num in numbers)


def answer1(numbers):
    median = round(computeMedian(numbers))
    deltas = [abs(num - median) for num in numbers]
    return sum(deltas)


def answer2(numbers):
    mean = round(sum(numbers) / len(numbers))
    cpt = 0
    found = False
    center = mean
    while cpt < 10 and not found:
        cpt += 1
        fuel = computeFuel(numbers, center)
        fuelPlus = computeFuel(numbers, center + 1)
        if fuelPlus < fuel:
            center = center + 1
        else:
            fuelMinus = computeFuel(numbers, center - 1)
            if fuelMinus < fuel:
                center = center - 1
            else:
                return fuel


print(answer1(lines))
print(answer2(lines))
