import os
from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    lines = [list(map(int, line.split(","))) for line in inputFile.readlines()][0]


def answer(numbers, days):
    fishes = Counter(numbers)
    for day in range(days):
        newFishes = Counter()
        for dayLeft, amount in fishes.items():
            newFishes[dayLeft - 1] = amount
        newFishes[6] += newFishes[-1]
        newFishes[8] += newFishes[-1]
        newFishes[-1] = 0
        fishes = newFishes
    return sum(fishes.values())

print(answer(lines, 80))
print(answer(lines, 256))
