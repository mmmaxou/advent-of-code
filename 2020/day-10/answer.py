import os
import operator
from itertools import tee
from functools import reduce
from collections import Counter, deque

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [int(line.strip()) for line in inputFile.readlines() if line.strip()]


def createChargersList(lines, reverse=False):
    return sorted([0] + lines + [max(lines) + 3], reverse=reverse)


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def getNextValues(iterable, n, startIndex=0):
    return iterable[slice(startIndex, startIndex + n)]


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def solve1():
    # copyList = initialLines.copy()
    # copyList.append(max(copyList) + 3)
    # listSorted = sorted(copyList)
    # listPairwise = [group for group in pairwise(listSorted)]
    # listDifferences = [b - a for a, b in listPairwise]
    # counterDifferences = Counter(listDifferences)
    # total = counterDifferences[1] * counterDifferences[3]

    # Why do 10 lines, when you can do 1 ??
    return prod(iter(Counter(b - a for a, b in pairwise(createChargersList(initialLines))).values()))


"""
numbers.push(numbers[numbers.length - 1] + 3)
let stepPossibilities = { 0: 1 }

numbers.forEach((a, i) => {
    numbers
        .slice(i + 1, i + 4)
        .filter(b => b - a <= 3)
        .forEach((_, j) => {
            stepPossibilities[i + 1 + j] = (stepPossibilities[i + 1 + j] || 0) + stepPossibilities[i]
        })        
})

// 2
console.log(stepPossibilities[numbers.length - 1])
"""


def solve2():
    stepPossibilities = {0: 1}
    chargers = createChargersList(initialLines, reverse=False)

    for i, a in enumerate(chargers):
        next3 = chargers[i + 1 : i + 4]
        filtered = [b for b in next3 if b - a <= 3]
        for _, j in enumerate(filtered):
            key = i + j + 1
            stepPossibilities[key] = stepPossibilities.get(key, 0) + stepPossibilities.get(i, 0)

    return stepPossibilities[len(chargers) - 1]


# print(solve1())
print(solve2())
