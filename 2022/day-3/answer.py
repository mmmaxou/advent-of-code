import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import iterateNumberwise

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]

PRIORITY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def getCommonItem(iterable):
    return set.intersection(*[set(i) for i in iterable])


def answer(iterable):
    sumPriority = 0
    for rucksack in iterable:
        compartments = [rucksack[0: len(rucksack) // 2], rucksack[len(rucksack) // 2: len(rucksack)]]
        commonItemsValues = [PRIORITY.index(item) + 1 for item in getCommonItem(compartments)]
        sumPriority += sum(commonItemsValues)
    return sumPriority


def answer2(iterable, numberwise):
    sumPriority = 0
    for elfGroup in iterateNumberwise(iterable, numberwise):
        commonItemsValues = [PRIORITY.index(item) + 1 for item in getCommonItem(elfGroup)]
        sumPriority += sum(commonItemsValues)
    return sumPriority

print(answer(lines))
print(answer2(lines, 3))
