import os
from functools import reduce
from itertools import combinations

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = set([int(line) for line in inputFile.readlines() if line])


def allSum(iterable):
    return reduce(lambda a, b: a + b, iterable)


def allMult(iterable):
    return reduce(lambda a, b: a * b, iterable)


def getCombination(iterable, factor):
    return {allSum(c): c for c in combinations(lines, factor)}


def answer(iterable, total, factor):
    return allMult(getCombination(iterable, factor).get(total))


print(answer(lines, 2020, 2))
print(answer(lines, 2020, 3))
